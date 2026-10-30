from __future__ import annotations

from collections.abc import Iterable
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .config import ParserConfig
from .models import Product


def clean(value: str) -> str:
    return " ".join(value.split())


def parse_page(html: str, config: ParserConfig, page_url: str = "") -> tuple[list[Product], int]:
    soup = BeautifulSoup(html, "html.parser")
    products: list[Product] = []
    skipped = 0
    base = config.base_url or page_url

    for node in soup.select(config.item):
        values: dict[str, str] = {}
        missing_required = False
        for name, spec in config.fields.items():
            element = node.select_one(spec.selector)
            if element is None:
                if spec.required:
                    missing_required = True
                    break
                values[name] = ""
                continue
            if spec.attr:
                values[name] = clean(element.get(spec.attr, ""))
            else:
                values[name] = clean(element.get_text(" ", strip=True))
        if missing_required:
            skipped += 1
            continue

        url = values.get("url", "")
        if url:
            url = urljoin(base, url)
        products.append(Product(
            title=values.get("title", ""),
            price=values.get("price", ""),
            url=url,
            sku=values.get("sku", ""),
            source=page_url,
        ))
    return products, skipped


def parse_pages(
    pages: Iterable[tuple[str, str]],
    config: ParserConfig,
) -> tuple[list[Product], dict[str, int]]:
    products: list[Product] = []
    seen: set[str] = set()
    stats = {"pages": 0, "found": 0, "skipped": 0, "duplicates": 0}

    for html, page_url in pages:
        stats["pages"] += 1
        page_products, skipped = parse_page(html, config, page_url)
        stats["found"] += len(page_products)
        stats["skipped"] += skipped
        for product in page_products:
            key = product.url or f"{product.title}\0{product.price}"
            if key in seen:
                stats["duplicates"] += 1
                continue
            seen.add(key)
            products.append(product)

    return products, stats

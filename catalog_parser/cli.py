from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests

from .config import ParserConfig
from .export import write_csv, write_xlsx
from .extract import parse_pages


def fetch(url: str, timeout: int = 20) -> str:
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "kwork-parser-demo/1.0 (+local test)"},
    )
    response.raise_for_status()
    response.encoding = response.apparent_encoding or response.encoding
    return response.text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="catalog-parser",
        description="Разобрать локальные HTML-страницы или URL в CSV/XLSX по конфигу.",
    )
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--html", action="append", default=[], type=Path)
    parser.add_argument("--url", action="append", default=[])
    parser.add_argument("--out", type=Path, default=Path("products.csv"))
    parser.add_argument("--xlsx", type=Path)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.html and not args.url:
        parser.error("give at least one --html or --url")

    try:
        config = ParserConfig.from_file(args.config)
        pages: list[tuple[str, str]] = []
        for path in args.html:
            pages.append((Path(path).read_text(encoding="utf-8"), f"file://{Path(path).resolve()}"))
        for url in args.url:
            pages.append((fetch(url), url))

        products, stats = parse_pages(pages, config)
        if args.limit is not None:
            products = products[: args.limit]

        write_csv(products, args.out)
        if args.xlsx:
            write_xlsx(products, args.xlsx)

        result = {
            "out": str(args.out),
            "xlsx": str(args.xlsx) if args.xlsx else None,
            "products": len(products),
            "stats": stats,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else _text(result))
        return 0
    except (OSError, ValueError, RuntimeError, requests.RequestException) as error:
        parser.exit(2, f"error: {error}\n")
    return 2


def _text(result: dict) -> str:
    stats = result["stats"]
    return "\n".join([
        f"pages: {stats['pages']}",
        f"found: {stats['found']}",
        f"duplicates: {stats['duplicates']}",
        f"skipped: {stats['skipped']}",
        f"products: {result['products']}",
        f"out: {result['out']}",
    ])

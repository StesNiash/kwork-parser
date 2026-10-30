from __future__ import annotations

import csv
from pathlib import Path

from .models import Product


FIELDS = ("sku", "title", "price", "url", "source")


def write_csv(products: list[Product], path: Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for product in products:
            writer.writerow(product.as_dict())


def write_xlsx(products: list[Product], path: Path) -> None:
    try:
        from openpyxl import Workbook
    except ImportError as error:
        raise RuntimeError("xlsx export requires: pip install openpyxl") from error

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "products"
    sheet.append(list(FIELDS))
    for product in products:
        data = product.as_dict()
        sheet.append([data[field] for field in FIELDS])
    workbook.save(path)

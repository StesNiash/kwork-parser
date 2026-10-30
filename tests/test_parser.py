import csv
import tempfile
import unittest
from pathlib import Path

from catalog_parser.config import ParserConfig
from catalog_parser.export import write_csv, write_xlsx
from catalog_parser.extract import parse_page, parse_pages

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "examples" / "config.json"
PAGE1 = ROOT / "tests" / "fixtures" / "page1.html"
PAGE2 = ROOT / "tests" / "fixtures" / "page2.html"


class ParserTests(unittest.TestCase):
    def setUp(self):
        self.config = ParserConfig.from_file(CONFIG)

    def test_parses_one_page_and_cleans_text(self):
        products, skipped = parse_page(PAGE1.read_text(encoding="utf-8"), self.config)
        self.assertEqual(skipped, 0)
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0].title, "Кружка керамическая")
        self.assertEqual(products[1].title, "Термос стальной")
        self.assertEqual(products[0].url, "https://shop.example/p/mug")

    def test_pagination_dedupe_and_skipped_card(self):
        pages = [
            (PAGE1.read_text(encoding="utf-8"), "page1"),
            (PAGE2.read_text(encoding="utf-8"), "page2"),
        ]
        products, stats = parse_pages(pages, self.config)
        self.assertEqual(stats["pages"], 2)
        self.assertEqual(stats["found"], 4)
        self.assertEqual(stats["duplicates"], 1)
        self.assertEqual(stats["skipped"], 1)
        self.assertEqual([product.sku for product in products], ["A-101", "A-102", "A-103"])

    def test_csv_export(self):
        products, _ = parse_pages([(PAGE1.read_text(encoding="utf-8"), "page1")], self.config)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "products.csv"
            write_csv(products, path)
            with path.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["sku"], "A-101")
            self.assertEqual(rows[1]["url"], "https://shop.example/p/thermos")

    def test_xlsx_export_if_available(self):
        try:
            import openpyxl  # noqa: F401
        except ImportError:
            self.skipTest("openpyxl is not installed")
        products, _ = parse_pages([(PAGE1.read_text(encoding="utf-8"), "page1")], self.config)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "products.xlsx"
            write_xlsx(products, path)
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()

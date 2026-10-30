from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from catalog_parser.config import ParserConfig
from catalog_parser.export import write_csv, write_xlsx
from catalog_parser.extract import parse_pages

DEMO = ROOT / "demo"


def main() -> None:
    config = ParserConfig.from_file(ROOT / "examples" / "config.json")
    pages = [
        (
            (ROOT / "tests" / "fixtures" / "page1.html").read_text(encoding="utf-8"),
            "https://shop.example/page/1",
        ),
        (
            (ROOT / "tests" / "fixtures" / "page2.html").read_text(encoding="utf-8"),
            "https://shop.example/page/2",
        ),
    ]
    products, stats = parse_pages(pages, config)
    DEMO.mkdir(exist_ok=True)
    write_csv(products, DEMO / "products.csv")
    xlsx = None
    try:
        write_xlsx(products, DEMO / "products.xlsx")
        xlsx = "demo/products.xlsx"
    except RuntimeError:
        pass

    result = {
        "products": len(products),
        "stats": stats,
        "csv": "demo/products.csv",
        "xlsx": xlsx,
    }
    (DEMO / "report.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (DEMO / "index.html").write_text(render(products, stats, xlsx), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def render(products, stats: dict, xlsx: str | None) -> str:
    rows = "".join(
        "<tr>"
        f"<td>{html.escape(product.sku)}</td>"
        f"<td>{html.escape(product.title)}</td>"
        f"<td>{html.escape(product.price)}</td>"
        f"<td>{html.escape(product.url)}</td>"
        "</tr>"
        for product in products
    )
    xlsx_line = f"<li><code>{xlsx}</code></li>" if xlsx else ""
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>kwork-parser — демо</title>
<style>
:root {{ color-scheme: dark; --bg:#090b10; --panel:#12151c; --line:#29303b; --text:#f4f0e8; --muted:#a6aab2; --gold:#f0c45c; --blue:#81b4ff; --green:#77d7a8; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:radial-gradient(circle at 82% 0%,rgba(129,180,255,.12),transparent 34rem),var(--bg); color:var(--text); font:15px/1.55 Inter,"Segoe UI",system-ui,sans-serif; }}
main {{ width:min(calc(100% - 40px),1000px); margin:auto; padding:56px 0; }}
.eyebrow {{ margin:0 0 10px; color:var(--gold); font-size:12px; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }}
h1 {{ margin:0 0 12px; font-size:clamp(36px,6vw,66px); line-height:.98; letter-spacing:-.05em; }}
.lead {{ max-width:740px; color:var(--muted); font-size:18px; }}
.stats {{ display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin:28px 0; }}
.stat {{ padding:16px; border:1px solid var(--line); border-radius:14px; background:var(--panel); }}
.stat span {{ display:block; color:var(--muted); font-size:12px; }}
.stat strong {{ font-size:26px; }}
.panel {{ margin:12px 0; padding:20px; border:1px solid var(--line); border-radius:16px; background:var(--panel); }}
.panel h2 {{ margin:0 0 10px; font-size:18px; }}
.panel p {{ margin:0 0 12px; color:var(--muted); }}
pre, code {{ font-family:"Cascadia Code",Consolas,monospace; }}
pre {{ margin:0; padding:12px; overflow:auto; border:1px solid var(--line); border-radius:10px; background:#0c0f14; color:var(--green); font-size:12px; }}
table {{ width:100%; border-collapse:collapse; font-size:13px; }}
th,td {{ padding:9px 8px; border-bottom:1px solid var(--line); text-align:left; vertical-align:top; }}
th {{ color:var(--muted); font-weight:600; }}
td:nth-child(1) {{ color:var(--blue); }}
.footer {{ margin-top:26px; color:#777b84; font-size:12px; }}
@media (max-width:720px) {{ .stats {{ grid-template-columns:1fr 1fr; }} }}
</style>
</head>
<body><main>
<p class="eyebrow">kwork-parser · demo report</p>
<h1>Каталог в CSV, без сюрпризов</h1>
<p class="lead">Две страницы, пять карточек, один дубль и одна битая карточка. Парсер оставил три валидных товара и честно показал, что пропустил.</p>
<div class="stats">
  <div class="stat"><span>страниц</span><strong>{stats['pages']}</strong></div>
  <div class="stat"><span>валидных</span><strong>{stats['found']}</strong></div>
  <div class="stat"><span>дублей</span><strong>{stats['duplicates']}</strong></div>
  <div class="stat"><span>пропущено</span><strong>{stats['skipped']}</strong></div>
</div>
<section class="panel"><h2>Команда</h2><pre>python -m catalog_parser --config examples/config.json \\
  --html tests/fixtures/page1.html --html tests/fixtures/page2.html \\
  --out demo/products.csv --xlsx demo/products.xlsx --json</pre></section>
<section class="panel"><h2>Результат</h2><table><thead><tr><th>SKU</th><th>Название</th><th>Цена</th><th>URL</th></tr></thead><tbody>{rows}</tbody></table></section>
<section class="panel"><h2>Файлы</h2><ul><li><code>demo/products.csv</code></li>{xlsx_line}</ul></section>
<p class="footer">Демо на локальных тестовых страницах. Никаких клиентских данных и секретов.</p>
</main></body></html>
"""


if __name__ == "__main__":
    main()

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Product:
    title: str
    price: str
    url: str
    sku: str = ""
    source: str = ""

    def as_dict(self) -> dict[str, str]:
        return asdict(self)

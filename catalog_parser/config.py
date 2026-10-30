from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FieldSpec:
    selector: str
    attr: str | None = None
    required: bool = False


@dataclass(frozen=True)
class ParserConfig:
    item: str
    fields: dict[str, FieldSpec]
    base_url: str = ""
    next_selector: str = ""

    @classmethod
    def from_file(cls, path: Path) -> "ParserConfig":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        fields = {}
        for name, raw in data["fields"].items():
            if isinstance(raw, str):
                fields[name] = FieldSpec(raw)
            else:
                fields[name] = FieldSpec(
                    selector=raw["selector"],
                    attr=raw.get("attr"),
                    required=bool(raw.get("required", False)),
                )
        if "item" not in data or not fields:
            raise ValueError("config must define item and fields")
        return cls(
            item=data["item"],
            fields=fields,
            base_url=data.get("base_url", ""),
            next_selector=data.get("next", ""),
        )

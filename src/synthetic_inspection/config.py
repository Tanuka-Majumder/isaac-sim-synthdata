from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class ProjectConfig:
    raw: dict[str, Any]
    source: Path

    @property
    def seed(self) -> int:
        return int(self.raw.get("project", {}).get("seed", 42))

    @property
    def output_dir(self) -> Path:
        configured = self.raw.get("export", {}).get("output_dir", "outputs/dataset")
        return Path(configured)


def load_config(path: str | Path) -> ProjectConfig:
    source = Path(path)
    with source.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Configuration at {source} must be a YAML mapping.")
    return ProjectConfig(raw=data, source=source)


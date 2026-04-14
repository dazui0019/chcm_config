from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_text_if_exists(path: Path, *, encoding: str = "utf-8") -> str | None:
    if not path.is_file():
        return None
    return path.read_text(encoding=encoding)


def write_text_if_changed(path: Path, content: str, *, encoding: str = "utf-8") -> bool:
    existing = read_text_if_exists(path, encoding=encoding)
    if existing == content:
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)
    return True


def load_pipeline_state(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}

    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Invalid pipeline state file: {path}")
    return raw


def save_pipeline_state(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

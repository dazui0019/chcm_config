from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


TEMPLATE_DIR = Path("templates")
OUTPUT_DIR = Path("output")
HEADER_TEMPLATE_DEFAULT = TEMPLATE_DIR / "app_config.h.tpl"
SOURCE_TEMPLATE_DEFAULT = TEMPLATE_DIR / "app_config.c.tpl"
HEADER_OUTPUT_DEFAULT = OUTPUT_DIR / "app_config.h"
SOURCE_OUTPUT_DEFAULT = OUTPUT_DIR / "app_config.c"
PLACEHOLDER_PATTERN = re.compile(r"@([A-Z0-9_]+)@")
PLACEHOLDER_NAME_PATTERN = re.compile(r"^[A-Z0-9_]+$")


def normalize_placeholder_name(name: str) -> str:
    if PLACEHOLDER_NAME_PATTERN.fullmatch(name):
        return name
    return re.sub(r"_+", "_", re.sub(r"[^A-Z0-9]+", "_", name.upper())).strip("_")


def stringify_context_value(name: str, value: Any) -> str:
    if value is None:
        raise ValueError(f"占位符 {name} 的值不能是 null。")
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    raise ValueError(f"占位符 {name} 的值类型不支持: {type(value).__name__}")


def load_mapping(raw: Any, section_name: str) -> dict[str, str]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError(f"{section_name} 必须是 JSON 对象。")
    return {
        normalize_placeholder_name(key): stringify_context_value(key, value)
        for key, value in raw.items()
    }


def load_render_context(context_path: Path) -> dict[str, str]:
    raw = json.loads(context_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("render context 顶层必须是 JSON 对象。")

    top_level = {
        key: value
        for key, value in raw.items()
        if key not in {"sections", "placeholders"} and not isinstance(value, (dict, list))
    }

    context = load_mapping(top_level, "render context")
    context.update(load_mapping(raw.get("placeholders"), "placeholders"))
    context.update(load_mapping(raw.get("sections"), "sections"))
    return context


def render_template(template_path: Path, context: dict[str, str]) -> str:
    template_text = template_path.read_text(encoding="utf-8")
    placeholders = set(PLACEHOLDER_PATTERN.findall(template_text))
    missing = sorted(name for name in placeholders if name not in context)
    if missing:
        formatted = ", ".join(missing)
        raise ValueError(f"{template_path} 缺少占位符值: {formatted}")
    return PLACEHOLDER_PATTERN.sub(lambda match: context[match.group(1)], template_text)


def write_rendered_file(output_path: Path, content: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render app_config.c/.h from a merged JSON render context.")
    parser.add_argument(
        "--context",
        type=Path,
        required=True,
        help="Merged render context JSON path.",
    )
    parser.add_argument(
        "--header-template",
        type=Path,
        default=HEADER_TEMPLATE_DEFAULT,
        help=f"Header template path. Default: {HEADER_TEMPLATE_DEFAULT}",
    )
    parser.add_argument(
        "--source-template",
        type=Path,
        default=SOURCE_TEMPLATE_DEFAULT,
        help=f"Source template path. Default: {SOURCE_TEMPLATE_DEFAULT}",
    )
    parser.add_argument(
        "--header-output",
        type=Path,
        default=HEADER_OUTPUT_DEFAULT,
        help=f"Rendered header output path. Default: {HEADER_OUTPUT_DEFAULT}",
    )
    parser.add_argument(
        "--source-output",
        type=Path,
        default=SOURCE_OUTPUT_DEFAULT,
        help=f"Rendered source output path. Default: {SOURCE_OUTPUT_DEFAULT}",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    context = load_render_context(args.context)

    rendered_header = render_template(args.header_template, context)
    rendered_source = render_template(args.source_template, context)

    write_rendered_file(args.header_output, rendered_header)
    write_rendered_file(args.source_output, rendered_source)

    print(f"Context: {args.context}")
    print(f"Wrote {args.header_output}")
    print(f"Wrote {args.source_output}")


if __name__ == "__main__":
    main()

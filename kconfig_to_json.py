from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from kconfiglib import BOOL, HEX, INT, STRING, TRISTATE, TYPE_TO_STR, Kconfig


KCONFIG_FILE_DEFAULT = Path("Kconfig")
CONFIG_FILE_DEFAULT = Path(".config")
OUTPUT_DEFAULT = Path("output") / "Kconfig.json"
OUTPUT_SCHEMA_VERSION = 1
PROJECT_SYMBOLS = ("PROJECT_A_SMALL", "PROJECT_A_PLUS_PLUS", "PROJECT_A_PLUS")
VERSION_SYMBOLS = ("COM_VERSION_V4", "COM_VERSION_V5")
VERSION_PLACEHOLDER_MAP = {
    "COM_VERSION_V4": "VERSION_V4",
    "COM_VERSION_V5": "VERSION_V5",
}


def is_json_scalar(value: Any) -> bool:
    return value is None or isinstance(value, (bool, int, float, str))


def render_json_compact(value: Any, indent: int = 0) -> str:
    if is_json_scalar(value):
        return json.dumps(value, ensure_ascii=False)

    if isinstance(value, list):
        if not value:
            return "[]"
        if all(is_json_scalar(item) for item in value):
            return json.dumps(value, ensure_ascii=False)

        child_indent = indent + 2
        rendered_items = [
            f"{' ' * child_indent}{render_json_compact(item, child_indent)}"
            for item in value
        ]
        return "[\n" + ",\n".join(rendered_items) + "\n" + (" " * indent) + "]"

    if isinstance(value, dict):
        if not value:
            return "{}"

        child_indent = indent + 2
        rendered_items = [
            f"{' ' * child_indent}{json.dumps(str(key), ensure_ascii=False)}: {render_json_compact(item, child_indent)}"
            for key, item in value.items()
        ]
        return "{\n" + ",\n".join(rendered_items) + "\n" + (" " * indent) + "}"

    raise TypeError(f"Unsupported JSON value type: {type(value).__name__}")


def coerce_symbol_value(symbol) -> Any:
    symbol_type = symbol.type
    value = symbol.str_value
    if symbol_type in {BOOL, TRISTATE}:
        return value == "y"
    if symbol_type in {INT, HEX}:
        if not value:
            return None
        return int(value, 0)
    if symbol_type == STRING:
        return value
    return value


def active_choice_symbol(symbols: dict[str, dict[str, Any]], names: tuple[str, ...]) -> str | None:
    for name in names:
        symbol = symbols.get(name)
        if symbol and symbol["value"] is True:
            return name
    return None


def build_output_payload(kconfig, kconfig_path: Path, config_path: Path) -> dict[str, Any]:
    symbols: dict[str, dict[str, Any]] = {}
    for name, symbol in sorted(kconfig.syms.items()):
        symbols[name] = {
            "type": TYPE_TO_STR.get(symbol.type, "unknown"),
            "value": coerce_symbol_value(symbol),
            "str_value": symbol.str_value,
        }

    project_name = active_choice_symbol(symbols, PROJECT_SYMBOLS)
    version_symbol = active_choice_symbol(symbols, VERSION_SYMBOLS)
    version_placeholder = VERSION_PLACEHOLDER_MAP.get(version_symbol)

    values = {
        "workbook_path": symbols.get("CHCM_WORKBOOK_PATH", {}).get("value"),
        "project_name": project_name,
        "project_id": symbols.get("PROJECT_NAME", {}).get("value"),
        "system_com_verion": version_placeholder,
        "system_com_verion_id": symbols.get("SYSTEM_COM_VERION", {}).get("value"),
        "eea_x": version_placeholder,
    }

    placeholders = {
        "PROJECT_NAME": project_name or "PROJECT_A_SMALL",
        "SYSTEM_COM_VERION": version_placeholder or "VERSION_V5",
        "EEA_X": version_placeholder or "VERSION_V5",
        "HB_LB_ANIMATION_ENABLE": symbols.get("HB_LB_ANIMATION_ENABLE", {}).get("value", False),
    }

    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "sheet_name": "Kconfig",
        "kconfig_file": str(kconfig_path),
        "config_file": str(config_path),
        "values": values,
        "symbols": symbols,
        "placeholders": placeholders,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert Kconfig/.config values to JSON.")
    parser.add_argument(
        "--kconfig",
        type=Path,
        default=KCONFIG_FILE_DEFAULT,
        help=f"Kconfig file path. Default: {KCONFIG_FILE_DEFAULT}",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=CONFIG_FILE_DEFAULT,
        help=f".config path. Default: {CONFIG_FILE_DEFAULT}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT_DEFAULT,
        help=f"Output JSON path. Default: {OUTPUT_DEFAULT}",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    kconfig = Kconfig(str(args.kconfig), warn=False)
    if args.config.is_file():
        kconfig.load_config(str(args.config))

    payload = build_output_payload(kconfig, args.kconfig, args.config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_json_compact(payload) + "\n", encoding="utf-8")

    print(f"Kconfig: {args.kconfig}")
    print(f"Config: {args.config}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

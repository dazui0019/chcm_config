from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet


WORKBOOK_DEFAULT = Path("xlsx") / "E01 CHCM-1C-2C1V(得邦)_config_Dataset_LEFT_V0.2.xlsx"
FIELD_KEYS = {
    "C": "config_word_0",
    "D": "value_1",
    "E": "value_2",
}
OUTPUT_VALUE_KEYS = {
    "config_word_0": "value_1",
    "value_1": "value_2",
    "value_2": "value_3",
}
FIELD_LABELS = {
    "config_word_0": "配置字0",
    "value_1": "配置值1",
    "value_2": "配置值2",
}
VALUE_LIKE_PATTERN = re.compile(
    r"^(?:/|others|reserved|inactive|"
    r"\d+(?:\.\d+)?(?:\s*\(default\))?|"
    r"\d+(?:\.\d+)?-\d+(?:\.\d+)?(?:\s*\(default\))?)$",
    re.IGNORECASE,
)
DEFAULT_MARKER_PATTERN = re.compile(r"\s*\(default\)\s*", re.IGNORECASE)


def normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).replace("\r\n", "\n").strip()
    return text or None


def normalize_field_value(value: str | None) -> str | None:
    if value in {None, "/"}:
        return None
    return value


def clean_output_value(value: str) -> str:
    return DEFAULT_MARKER_PATTERN.sub("", value).strip()


def has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def is_value_like(text: str | None) -> bool:
    if text is None:
        return False
    return bool(VALUE_LIKE_PATTERN.fullmatch(text))


def is_label_like(text: str | None) -> bool:
    if text is None:
        return False
    if is_value_like(text):
        return False
    if has_cjk(text):
        return True
    return bool(re.fullmatch(r"Value\d+", text, re.IGNORECASE))


def is_item_start(item_code: str | None) -> bool:
    return bool(item_code and item_code.isdigit())


def row_snapshot(worksheet: Worksheet, row_index: int) -> dict[str, Any]:
    return {
        "source_row": row_index,
        "item_code": normalize_text(worksheet[f"A{row_index}"].value),
        "item_name": normalize_text(worksheet[f"B{row_index}"].value),
        "config_word_0": normalize_field_value(normalize_text(worksheet[f"C{row_index}"].value)),
        "value_1": normalize_field_value(normalize_text(worksheet[f"D{row_index}"].value)),
        "value_2": normalize_field_value(normalize_text(worksheet[f"E{row_index}"].value)),
        "description": normalize_text(worksheet[f"F{row_index}"].value),
    }


def row_has_content(row: dict[str, Any]) -> bool:
    return any(row[key] is not None for key in ("item_code", "item_name", "config_word_0", "value_1", "value_2", "description"))


def row_has_label_fields(row: dict[str, Any]) -> bool:
    present = [row[key] for key in FIELD_LABELS if row[key] is not None]
    if not present:
        return False
    return all(is_label_like(value) for value in present)


def extract_values(row: dict[str, Any]) -> dict[str, str]:
    return {key: row[key] for key in FIELD_LABELS if row[key] is not None}


def build_field_labels(
    used_keys: set[str],
    explicit_labels: dict[str, str] | None = None,
) -> dict[str, str]:
    explicit_labels = explicit_labels or {}
    return {key: explicit_labels.get(key, FIELD_LABELS[key]) for key in FIELD_LABELS if key in used_keys}


def detail_row_payload(row: dict[str, Any]) -> dict[str, Any]:
    payload: dict[str, Any] = {"source_row": row["source_row"]}
    for key in FIELD_LABELS:
        if row[key] is not None:
            payload[key] = row[key]
    if row["description"] is not None:
        payload["description"] = row["description"]
    return payload


def detect_used_keys(*sections: Any) -> set[str]:
    used: set[str] = set()
    for section in sections:
        if isinstance(section, dict):
            for key in FIELD_LABELS:
                if section.get(key) is not None:
                    used.add(key)
        elif isinstance(section, list):
            for item in section:
                if not isinstance(item, dict):
                    continue
                for key in FIELD_LABELS:
                    if item.get(key) is not None:
                        used.add(key)
    return used


def explicit_labels_from_row(row: dict[str, Any] | None) -> dict[str, str]:
    if row is None:
        return {}
    labels: dict[str, str] = {}
    for key in FIELD_LABELS:
        value = row[key]
        if is_label_like(value):
            labels[key] = value
    return labels


def classify_detail_rows(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not rows:
        return [], []
    if all(row_has_label_fields(row) for row in rows):
        return [detail_row_payload(row) for row in rows], []
    return [], [detail_row_payload(row) for row in rows]


def parse_config_block(top_row: dict[str, Any], detail_rows: list[dict[str, Any]]) -> dict[str, Any]:
    remaining_rows = [row for row in detail_rows if row_has_content(row)]
    explicit_labels = explicit_labels_from_row(top_row)
    defaults: dict[str, str] = {}
    definitions: list[dict[str, Any]] = []
    options: list[dict[str, Any]] = []
    input_hint = top_row["description"]
    structure_type = "free_input"

    if explicit_labels:
        defaults_row = None
        if remaining_rows and remaining_rows[0]["item_code"] is None and remaining_rows[0]["item_name"] is None:
            defaults_row = remaining_rows.pop(0)
            defaults = extract_values(defaults_row)
        if defaults_row and defaults_row["description"]:
            input_hint = defaults_row["description"]

        definitions, options = classify_detail_rows(remaining_rows)
        structure_type = "mapping_table" if options else "free_input"
        if defaults:
            structure_type = "composite_select" if options else "composite_input"
    else:
        defaults = extract_values(top_row)
        definitions, options = classify_detail_rows(remaining_rows)
        if options:
            structure_type = "select"
        elif definitions:
            structure_type = "free_input"

        if definitions and not input_hint:
            definition_descriptions = [row.get("description") for row in definitions if row.get("description")]
            if definition_descriptions:
                input_hint = definition_descriptions[0]

    definition_labels = explicit_labels_from_row(remaining_rows[0]) if definitions and remaining_rows else {}
    used_keys = detect_used_keys(defaults, definitions, options)
    field_labels = build_field_labels(used_keys, explicit_labels or definition_labels)

    item = {
        "id": int(top_row["item_code"]),
        "name": top_row["item_name"],
        "structure_type": structure_type,
        "source_row_start": top_row["source_row"],
        "field_labels": field_labels,
    }

    if defaults:
        item["defaults"] = defaults
    if input_hint:
        item["input_hint"] = input_hint
    if definitions:
        item["definitions"] = definitions
    if options:
        item["options"] = options
    return item


def parse_hcm_prilin_matrix(worksheet: Worksheet) -> dict[str, Any]:
    rows = [row_snapshot(worksheet, row_index) for row_index in range(1, worksheet.max_row + 1)]
    rows = [row for row in rows if row_has_content(row)]

    start_indices = [index for index, row in enumerate(rows) if is_item_start(row["item_code"])]
    if not start_indices:
        raise ValueError("未找到配置项块。")

    header_row = rows[0]
    first_positive_index = next(
        (index for index, row in enumerate(rows) if is_item_start(row["item_code"]) and row["item_code"] != "0"),
        None,
    )
    global_note_row_numbers = {
        row["source_row"]
        for row in rows[1:first_positive_index]
        if row["item_code"] is None
        and row["item_name"] is None
        and all(row[key] is None for key in FIELD_LABELS)
        and row["description"] is not None
    }
    notes = [row["description"] for row in rows if row["source_row"] in global_note_row_numbers]

    items: list[dict[str, Any]] = []
    for position, start_index in enumerate(start_indices):
        end_index = start_indices[position + 1] if position + 1 < len(start_indices) else len(rows)
        block_rows = rows[start_index:end_index]
        detail_rows = [row for row in block_rows[1:] if row["source_row"] not in global_note_row_numbers]
        items.append(parse_config_block(block_rows[0], detail_rows))

    result = {
        "parser": "hcm_prilin_matrix",
        "sheet_name_raw": worksheet.title,
        "sheet_name": worksheet.title.strip(),
        "header": {
            "item_code": header_row["item_code"],
            "item_name": header_row["item_name"],
            **{FIELD_KEYS[column]: normalize_text(worksheet[f"{column}{header_row['source_row']}"].value) for column in FIELD_KEYS},
            "description": header_row["description"],
        },
        "items": items,
    }

    if notes:
        result["notes"] = notes
    return result


def relabel_values(field_labels: dict[str, str], values: dict[str, str]) -> dict[str, str]:
    del field_labels
    return {
        OUTPUT_VALUE_KEYS[key]: clean_output_value(value)
        for key, value in values.items()
        if value is not None
    }


def option_to_value_row(item: dict[str, Any], option: dict[str, Any]) -> dict[str, str]:
    raw_values = {key: option[key] for key in FIELD_LABELS if option.get(key) is not None}
    return relabel_values(item.get("field_labels", {}), raw_values)


def condense_hcm_prilin_matrix(parsed: dict[str, Any]) -> dict[str, Any]:
    condensed_items: list[dict[str, Any]] = []
    for item in parsed["items"]:
        condensed_item = {
            "id": item["id"],
            "name": item["name"],
        }

        defaults = item.get("defaults", {})
        options = item.get("options", [])
        if defaults:
            condensed_item["values"] = relabel_values(item.get("field_labels", {}), defaults)
        elif options:
            condensed_item["values"] = [option_to_value_row(item, option) for option in options]
        else:
            condensed_item["values"] = {}

        condensed_items.append(condensed_item)

    return {
        "sheet_name": parsed["sheet_name"],
        "items": condensed_items,
    }


def find_sheet_path(workbook_path: Path, requested_sheet: str) -> Worksheet:
    workbook = load_workbook(workbook_path, data_only=False)
    matches = [sheet for sheet in workbook.worksheets if sheet.title.strip() == requested_sheet.strip()]
    if not matches:
        available = ", ".join(repr(sheet.title) for sheet in workbook.worksheets)
        raise ValueError(f"未找到 sheet: {requested_sheet!r}。可用 sheet: {available}")
    if len(matches) > 1:
        names = ", ".join(repr(sheet.title) for sheet in matches)
        raise ValueError(f"去空格后存在重名 sheet: {names}")
    return matches[0]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert CHCM workbook sheets to JSON.")
    parser.add_argument(
        "--workbook",
        type=Path,
        default=WORKBOOK_DEFAULT,
        help=f"Workbook path. Default: {WORKBOOK_DEFAULT}",
    )
    parser.add_argument(
        "--sheet",
        default="HCM_PriLIN_Matrix",
        help="Sheet name. Leading and trailing spaces are ignored when matching.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output") / "HCM_PriLIN_Matrix.json",
        help="Output JSON path.",
    )
    parser.add_argument(
        "--mode",
        choices=("values", "full"),
        default="values",
        help="Output only config items and values, or the full parsed structure.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    worksheet = find_sheet_path(args.workbook, args.sheet)

    sheet_name = worksheet.title.strip()
    if sheet_name != "HCM_PriLIN_Matrix":
        raise ValueError(f"当前仅支持 HCM_PriLIN_Matrix，实际匹配到 {worksheet.title!r}")

    parsed = parse_hcm_prilin_matrix(worksheet)
    output_payload = condense_hcm_prilin_matrix(parsed) if args.mode == "values" else parsed
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output_payload, ensure_ascii=False, indent=2), encoding="utf-8")
    item_count = len(output_payload["items"]) if "items" in output_payload else len(parsed["items"])

    print(f"Wrote {args.output}")
    print(f"Sheet: {parsed['sheet_name_raw']!r}")
    print(f"Items: {item_count}")
    print(f"Mode: {args.mode}")


if __name__ == "__main__":
    main()

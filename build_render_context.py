from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


INPUT_DIR_DEFAULT = Path("output")
KCONFIG_JSON_DEFAULT = INPUT_DIR_DEFAULT / "Kconfig.json"
OUTPUT_DEFAULT = INPUT_DIR_DEFAULT / "render_context.json"
HEADER_TEMPLATE_DEFAULT = Path("templates") / "app_config.h.tpl"
SOURCE_TEMPLATE_DEFAULT = Path("templates") / "app_config.c.tpl"
OUTPUT_SCHEMA_VERSION = 1
PLACEHOLDER_PATTERN = re.compile(r"@([A-Z0-9_]+)@")
BLOCK_PLACEHOLDER_TOKENS = ("DEFINITION", "DEFINITIONS", "DECLARATION", "DECLARATIONS", "MACRO", "MACROS")
SCALAR_DEFAULTS = {
    "PROJECT_NAME": "PROJECT_A_SMALL",
    "SYSTEM_COM_VERION": "VERSION_V5",
    "EEA_X": "VERSION_V5",
    "USED_MATRIX_CHIP_NUMS": 0,
    "USED_MATRIX_LED_NUMS": 0,
    "USED_CVCC_CHIP_NUMS": 0,
    "CVCC_OUTPUT_VOLTAGE_LEVELS": 18,
    "SIGNAL_LED_CURRENT_METHOD": 1,
    "TI_DRL_CURRENT_DERATE_METHOD": 0,
    "TI_USED_LED_NUMS": 0,
    "TI_USED_LED_NUMS_DATA_LENS": 0,
    "TI_SWEEP_CYCLE_TIME": 0,
    "TI_SWEEP_USER_STEP": 0,
    "TI_SWEEP_STEP_MAX": 0,
    "TI_SEEP_ANIMATION_MODE": 2,
}
CHCM_CFG_ITEM_COUNT = 27
CHCM_CFG_DEFAULT_NAME = {
    0: "Inactive",
    1: "信号灯LED额定电流",
    2: "LSD_Out1功能配置",
    3: "LSD_Out2功能配置",
    4: "HSD OUT1功能配置",
    5: "HSD OUT2功能配置",
    6: "HSD OUT3功能配置",
    7: "HSD OUT4功能配置",
    8: "LSD_IN1功能配置",
    9: "LSD_IN2功能配置",
    10: "BUCK CV芯片电压调整功能",
    11: "位置灯电流占空比设定",
    12: "日行灯降额配置",
    13: "近光灯降额配置",
    14: "远光灯降额配置",
    15: "位置灯延时配置",
    16: "高度调节电机类型",
    17: "直流电机四档电压值配置",
    18: "步进电机初始化运动配置",
    19: "步进电机堵转点到对应档位运动步数",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_excel_jsons(input_dir: Path, excluded_files: set[Path]) -> dict[str, dict[str, Any]]:
    excel_payloads: dict[str, dict[str, Any]] = {}
    for path in sorted(input_dir.glob("*.json")):
        if path.resolve() in excluded_files:
            continue
        payload = load_json(path)
        if not isinstance(payload, dict):
            continue
        sheet_name = payload.get("sheet_name") or path.stem
        if sheet_name in {"Kconfig", "render_context"}:
            continue
        excel_payloads[sheet_name] = payload
    return excel_payloads


def load_required_placeholders(*template_paths: Path) -> set[str]:
    placeholders: set[str] = set()
    for template_path in template_paths:
        placeholders.update(PLACEHOLDER_PATTERN.findall(template_path.read_text(encoding="utf-8")))
    return placeholders


def is_block_placeholder(name: str) -> bool:
    return any(token in name for token in BLOCK_PLACEHOLDER_TOKENS)


def extract_scalar_placeholders(kconfig_payload: dict[str, Any], excel_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    placeholders = dict(kconfig_payload.get("placeholders", {}))

    current_config = excel_payloads.get("current_config", {})
    ch_cfg = excel_payloads.get("CH_Cfg", {})
    ti_sequential = excel_payloads.get("TI_sequential", {})

    used_cvcc_ic_nums = current_config.get("total_ic_count")
    if used_cvcc_ic_nums is None:
        used_cvcc_ic_nums = ch_cfg.get("ic_count")
    if used_cvcc_ic_nums is not None:
        placeholders["USED_CVCC_CHIP_NUMS"] = used_cvcc_ic_nums

    frames = ti_sequential.get("animation", {}).get("frames", [])
    ti_channels = {
        channel_name
        for frame in frames
        for channel_name in frame.get("channels", {})
    }
    if ti_channels:
        placeholders["TI_USED_LED_NUMS"] = len(ti_channels)
        placeholders["TI_USED_LED_NUMS_DATA_LENS"] = math.ceil(len(ti_channels) / 32)

    if len(frames) >= 2:
        first_time = frames[0].get("time_ms")
        second_time = frames[1].get("time_ms")
        if isinstance(first_time, (int, float)) and isinstance(second_time, (int, float)):
            placeholders["TI_SWEEP_CYCLE_TIME"] = int(second_time - first_time)

    if frames:
        placeholders["TI_SWEEP_USER_STEP"] = max(len(frames) - 1, 0)
        placeholders["TI_SWEEP_STEP_MAX"] = max(len(frames) - 1, 0)

    return placeholders


def build_section_stub(name: str, excel_payloads: dict[str, dict[str, Any]]) -> str:
    sources = ", ".join(sorted(excel_payloads)) or "Kconfig"
    return f"/* TODO: populate {name} from merged JSON sources: {sources}. */"


def coerce_chcm_cfg_word(value: Any) -> int | None:
    if value is None:
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value) if value.is_integer() else None
    return None


def format_chcm_cfg_entry(words: list[int], comment: str) -> str:
    return f"    {{{words[0]}U, {words[1]}U, {words[2]}U}}, /**< {comment} */"


def build_chcm_cfg_definition(excel_payloads: dict[str, dict[str, Any]]) -> str:
    matrix_payload = excel_payloads.get("HCM_PriLIN_Matrix")
    if matrix_payload is None:
        raise ValueError("缺少 HCM_PriLIN_Matrix.json，无法生成 CHCM_Cfg 定义。")

    items_by_id = matrix_payload.get("items_by_id")
    if not isinstance(items_by_id, dict):
        raise ValueError("HCM_PriLIN_Matrix.json 缺少 items_by_id，无法生成 CHCM_Cfg 定义。")

    lines = [
        'const __attribute__ ((used,used,section(".parameter_config_48")))  CHCM_Cfg_T CHCM_Cfg[CHCM_CFG_IDX_MAX] = {'
    ]

    for item_id in range(CHCM_CFG_ITEM_COUNT):
        item = items_by_id.get(str(item_id), {})
        name = item.get("name") or CHCM_CFG_DEFAULT_NAME.get(item_id, f"保留{item_id}")
        entries = item.get("entries", [])
        words = [0, 0, 0]

        if len(entries) == 1 and isinstance(entries[0], dict):
            parsed_words: list[int] = []
            supported = True
            for key in ("value_1", "value_2", "value_3"):
                word = coerce_chcm_cfg_word(entries[0].get(key))
                if word is None:
                    supported = False
                    break
                parsed_words.append(word)
            if supported:
                words = parsed_words
                comment = f"Config item{item_id} {name}"
            else:
                comment = f"Config item{item_id} {name} (non-integer entry kept as 0U)"
        elif len(entries) > 1:
            comment = f"Config item{item_id} {name} (multi-entry item kept as 0U)"
        elif item_id >= 20:
            comment = f"Config item{item_id} 保留"
        else:
            comment = f"Config item{item_id} {name}"

        lines.append(format_chcm_cfg_entry(words, comment))

    lines.append("};                                     /* Referenced by: '<S5>/CHCM_Cfg' */")
    return "\n".join(lines)


def build_render_context(
    excel_payloads: dict[str, dict[str, Any]],
    kconfig_payload: dict[str, Any],
    required_placeholders: set[str],
) -> dict[str, Any]:
    placeholders = {**SCALAR_DEFAULTS, **extract_scalar_placeholders(kconfig_payload, excel_payloads)}
    sections: dict[str, str] = {}

    for name in sorted(required_placeholders):
        if is_block_placeholder(name):
            if name == "CHCM_CFG_DEFINITION":
                sections[name] = build_chcm_cfg_definition(excel_payloads)
            else:
                sections[name] = build_section_stub(name, excel_payloads)
            continue
        placeholders.setdefault(name, SCALAR_DEFAULTS.get(name, 0))

    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "sheet_name": "render_context",
        "placeholders": placeholders,
        "sections": sections,
        "excel": excel_payloads,
        "kconfig": kconfig_payload,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Merge Excel JSON and Kconfig JSON into render_context.json.")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=INPUT_DIR_DEFAULT,
        help=f"Excel JSON directory. Default: {INPUT_DIR_DEFAULT}",
    )
    parser.add_argument(
        "--kconfig-json",
        type=Path,
        default=KCONFIG_JSON_DEFAULT,
        help=f"Kconfig JSON path. Default: {KCONFIG_JSON_DEFAULT}",
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
        "--output",
        type=Path,
        default=OUTPUT_DEFAULT,
        help=f"Output render context path. Default: {OUTPUT_DEFAULT}",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    excluded_files = {args.kconfig_json.resolve(), args.output.resolve()}
    excel_payloads = load_excel_jsons(args.input_dir, excluded_files)
    kconfig_payload = load_json(args.kconfig_json)
    required_placeholders = load_required_placeholders(args.header_template, args.source_template)

    payload = build_render_context(excel_payloads, kconfig_payload, required_placeholders)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Input dir: {args.input_dir}")
    print(f"Kconfig JSON: {args.kconfig_json}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

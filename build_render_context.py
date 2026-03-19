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
CVCC_OUTPUT_VOLTAGE_CONFIGS = (
    ("5V0", 68, "5.0V"),
    ("5V2", 66, "5.2V"),
    ("5V4", 63, "5.4V"),
    ("5V6", 60, "5.6V"),
    ("5V8", 58, "5.8V"),
    ("6V0", 55, "6.0V"),
    ("6V2", 52, "6.2V"),
    ("6V4", 49, "6.4V"),
    ("6V6", 47, "6.6V"),
    ("6V8", 44, "6.8V"),
    ("7V0", 42, "7.0V"),
    ("7V2", 39, "7.2V"),
    ("7V4", 36, "7.4V"),
    ("7V6", 34, "7.6V"),
    ("7V8", 31, "7.8V"),
    ("8V0", 28, "8.0V"),
    ("8V2", 26, "8.2V"),
    ("8V4", 23, "8.4V"),
)
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
CHCM_CFG_INDEX_NAME_MAP = [
    ("CHCM_CFG_IDX_0_INACTIVE", "Inactive"),
    ("CHCM_CFG_IDX_1_SIGNAL_LED_CURRENT", "信号灯LED额定电流"),
    ("CHCM_CFG_IDX_2_LSD_OUT1", "LSD_Out1功能配置"),
    ("CHCM_CFG_IDX_3_LSD_OUT2", "LSD_Out2功能配置"),
    ("CHCM_CFG_IDX_4_HSD_OUT1", "HSD OUT1功能配置"),
    ("CHCM_CFG_IDX_5_HSD_OUT2", "HSD OUT2功能配置"),
    ("CHCM_CFG_IDX_6_HSD_OUT3", "HSD OUT3功能配置"),
    ("CHCM_CFG_IDX_7_HSD_OUT4", "HSD OUT4功能配置"),
    ("CHCM_CFG_IDX_8_LSD_IN1", "LSD_IN1功能配置"),
    ("CHCM_CFG_IDX_9_LSD_IN2", "LSD_IN2功能配置"),
    ("CHCM_CFG_IDX_10_BUCK_CV", "BUCK CV芯片电压调整功能"),
    ("CHCM_CFG_IDX_11_PL_DUTY", "位置灯电流占空比设定"),
    ("CHCM_CFG_IDX_12_DRL_NTC_DERATE", "日行灯降额配置"),
    ("CHCM_CFG_IDX_13_LB_NTC_DERATE", "近光灯降额配置"),
    ("CHCM_CFG_IDX_14_HB_NTC_DERATE", "远光灯降额配置"),
    ("CHCM_CFG_IDX_15_PL_DELAY", "位置灯延时配置"),
    ("CHCM_CFG_IDX_16_AFS_TYPE", "高度调节电机类型"),
    ("CHCM_CFG_IDX_17_DC_MOTOR_LEVEL", "直流电机四档电压值配置"),
    ("CHCM_CFG_IDX_18_STEP_MOTOR_INIT_DIR", "步进电机初始化运动配置"),
    ("CHCM_CFG_IDX_19_STEP_MOTOR_BLOCK_STEPS", "步进电机堵转点到对应档位运动步数"),
]
CHCM_CFG_FIXED_INDEX_VALUES = {
    "CHCM_CFG_IDX_20_RESERVED_20": 20,
    "CHCM_CFG_IDX_21_RESERVED_21": 21,
    "CHCM_CFG_IDX_22_RESERVED_22": 22,
    "CHCM_CFG_IDX_23_RESERVED_23": 23,
    "CHCM_CFG_IDX_24_RESERVED_24": 24,
    "CHCM_CFG_IDX_25_RESERVED_25": 25,
    "CHCM_CFG_IDX_26_RESERVED_26": 26,
}
MOTOR_CFG_DIRECTION_MACRO_MAP = {
    "push": "MOTOR_PUSH",
    "pull": "MOTOR_PULL",
}
MOTOR_CFG_STEP_MODE_MACRO_MAP = {
    "1/8[fs]": "MOTOR_STEP_MODE_1_8_STEP",
    "1/16[fs]": "MOTOR_STEP_MODE_1_16_STEP",
    "1/32[fs]": "MOTOR_STEP_MODE_1_32_STEP",
}
MOTOR_POSITION_KEYS = ("pos1", "pos2", "pos3", "pos4", "pos5")
MOTOR_AFS_LEVEL_KEYS = ("level0", "level1", "level2", "level3")
MOTOR_RUN_MODE_KEY_MAP = (
    ("reference_run", "Reference run"),
    ("normal_run", "Normal Operation"),
)
MOTOR_RUN_FIELD_KEYS = (
    "running_current",
    "holding_current",
    "max_acceleration_ramp",
    "min_speed",
    "normal_speed",
    "max_speed",
)
MOTOR_DC_LEVEL_CFG_ID = 17


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


def require_dict(parent: dict[str, Any], key: str, context: str) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{context} 缺少对象字段 {key!r}。")
    return value


def require_excel_payload(
    excel_payloads: dict[str, dict[str, Any]],
    sheet_name: str,
    *,
    purpose: str,
) -> dict[str, Any]:
    payload = excel_payloads.get(sheet_name)
    if not isinstance(payload, dict):
        raise ValueError(f"缺少 {sheet_name}.json，无法{purpose}。")
    return payload


def load_kconfig_symbols(kconfig_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    symbols = kconfig_payload.get("symbols")
    if not isinstance(symbols, dict):
        raise ValueError("Kconfig.json 缺少 symbols，无法生成 Kconfig 相关占位符。")
    return symbols


def read_kconfig_int_symbol(symbols: dict[str, dict[str, Any]], name: str, default: int) -> int:
    symbol = symbols.get(name)
    if not isinstance(symbol, dict):
        return default
    value = symbol.get("value")
    if value is None:
        return default
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"Kconfig 符号 {name} 必须是整数。")
    return value


def build_cvcc_output_voltage_placeholders(
    kconfig_payload: dict[str, Any],
    required_placeholders: set[str],
) -> dict[str, int]:
    voltage_placeholder_required = any(
        name == "CVCC_OUTPUT_VOLTAGE_LEVELS"
        or name.startswith("CVCC_OUTPUT_VOLTAGE_IDX_")
        or name.startswith("CVCC_OUTPUT_VOLTAGE_")
        for name in required_placeholders
    )
    if not voltage_placeholder_required:
        return {}

    symbols = load_kconfig_symbols(kconfig_payload)
    expected_levels = len(CVCC_OUTPUT_VOLTAGE_CONFIGS)
    configured_levels = read_kconfig_int_symbol(symbols, "CVCC_OUTPUT_VOLTAGE_LEVELS", expected_levels)
    if configured_levels != expected_levels:
        raise ValueError(
            f"CVCC_OUTPUT_VOLTAGE_LEVELS 必须等于 {expected_levels}，当前为 {configured_levels}。"
        )

    placeholders: dict[str, int] = {
        "CVCC_OUTPUT_VOLTAGE_LEVELS": configured_levels,
    }
    for index, (suffix, default_value, _comment) in enumerate(CVCC_OUTPUT_VOLTAGE_CONFIGS):
        placeholders[f"CVCC_OUTPUT_VOLTAGE_IDX_{suffix}"] = index
        placeholders[f"CVCC_OUTPUT_VOLTAGE_{suffix}"] = read_kconfig_int_symbol(
            symbols,
            f"CVCC_OUTPUT_VOLTAGE_{suffix}",
            default_value,
        )

    return placeholders


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


def format_chcm_cfg_index_value(value: int) -> str:
    return f"{value:2d}"


def load_chcm_cfg_sources(excel_payloads: dict[str, dict[str, Any]]) -> tuple[dict[str, int], dict[str, Any]]:
    matrix_payload = excel_payloads.get("HCM_PriLIN_Matrix")
    if matrix_payload is None:
        raise ValueError("缺少 HCM_PriLIN_Matrix.json，无法生成 CHCM_CFG 占位符。")

    items = matrix_payload.get("items", [])
    name_to_id = {
        item.get("name"): item.get("id")
        for item in items
        if isinstance(item, dict)
        and isinstance(item.get("name"), str)
        and isinstance(item.get("id"), int)
    }
    items_by_id = matrix_payload.get("items_by_id")
    if not isinstance(items_by_id, dict):
        raise ValueError("HCM_PriLIN_Matrix.json 缺少 items_by_id，无法生成 CHCM_CFG 占位符。")
    return name_to_id, items_by_id


def build_chcm_cfg_index_placeholders(name_to_id: dict[str, int]) -> dict[str, str]:
    placeholders: dict[str, str] = {}
    resolved_values: list[int] = []

    for macro_name, cfg_name in CHCM_CFG_INDEX_NAME_MAP:
        if cfg_name not in name_to_id:
            raise ValueError(f"Excel 中缺少 CFG 项 {cfg_name!r}，无法生成宏 {macro_name}。")
        value = name_to_id[cfg_name]
        placeholders[macro_name] = format_chcm_cfg_index_value(value)
        resolved_values.append(value)

    for macro_name, value in CHCM_CFG_FIXED_INDEX_VALUES.items():
        placeholders[macro_name] = format_chcm_cfg_index_value(value)
        resolved_values.append(value)

    placeholders["CHCM_CFG_IDX_MAX"] = format_chcm_cfg_index_value(max(resolved_values, default=-1) + 1)
    return placeholders

def resolve_chcm_cfg_entry(item_id: int, items_by_id: dict[str, Any]) -> tuple[list[int], str]:
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

    return words, comment


def build_chcm_cfg_item_placeholders(items_by_id: dict[str, Any]) -> dict[str, str]:
    placeholders: dict[str, str] = {}

    for item_id in range(CHCM_CFG_ITEM_COUNT):
        words, comment = resolve_chcm_cfg_entry(item_id, items_by_id)
        placeholders[f"CHCM_CFG_ITEM_{item_id}_WORD0"] = str(words[0])
        placeholders[f"CHCM_CFG_ITEM_{item_id}_WORD1"] = str(words[1])
        placeholders[f"CHCM_CFG_ITEM_{item_id}_WORD2"] = str(words[2])
        placeholders[f"CHCM_CFG_ITEM_{item_id}_COMMENT"] = comment

    return placeholders


def build_chcm_cfg_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, str]:
    needs_index_placeholders = any(
        name == "CHCM_CFG_IDX_MAX" or name.startswith("CHCM_CFG_IDX_")
        for name in required_placeholders
    )
    needs_item_placeholders = any(name.startswith("CHCM_CFG_ITEM_") for name in required_placeholders)
    if not needs_index_placeholders and not needs_item_placeholders:
        return {}

    name_to_id, items_by_id = load_chcm_cfg_sources(excel_payloads)
    placeholders: dict[str, str] = {}
    if needs_index_placeholders:
        placeholders.update(build_chcm_cfg_index_placeholders(name_to_id))
    if needs_item_placeholders:
        placeholders.update(build_chcm_cfg_item_placeholders(items_by_id))
    return placeholders


def round_half_away_from_zero(value: float) -> int:
    if value >= 0:
        return math.floor(value + 0.5)
    return math.ceil(value - 0.5)


def scale_motor_numeric(value: Any, scale: int, field_name: str) -> int:
    if value is None or isinstance(value, bool):
        raise ValueError(f"Motor_Cfg 字段 {field_name} 缺少有效数值。")
    if isinstance(value, (int, float)):
        numeric = float(value)
    elif isinstance(value, str):
        try:
            numeric = float(value.strip())
        except ValueError as exc:
            raise ValueError(f"Motor_Cfg 字段 {field_name} 不是数值: {value!r}") from exc
    else:
        raise ValueError(f"Motor_Cfg 字段 {field_name} 的值类型不支持: {type(value).__name__}")
    return round_half_away_from_zero(numeric * scale)


def resolve_motor_direction_macro(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Motor_Cfg.general_settings.positive_command_action 必须是字符串。")
    normalized = value.strip().lower()
    if normalized not in MOTOR_CFG_DIRECTION_MACRO_MAP:
        raise ValueError(f"不支持的电机方向配置: {value!r}")
    return MOTOR_CFG_DIRECTION_MACRO_MAP[normalized]


def resolve_motor_step_mode_macro(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("Motor_Cfg.microstep_mode 必须是字符串。")
    normalized = value.strip().lower()
    if normalized not in MOTOR_CFG_STEP_MODE_MACRO_MAP:
        raise ValueError(f"不支持的步进模式: {value!r}")
    return MOTOR_CFG_STEP_MODE_MACRO_MAP[normalized]


def load_motor_config_sources(excel_payloads: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], dict[str, Any]]:
    motor_payload = require_excel_payload(excel_payloads, "Motor_Cfg", purpose="生成 Motor 配置占位符")
    motor_config = motor_payload.get("motor_config")
    if not isinstance(motor_config, dict):
        raise ValueError("Motor_Cfg.json 缺少 motor_config，无法生成 Motor 配置占位符。")

    _, items_by_id = load_chcm_cfg_sources(excel_payloads)
    return motor_config, items_by_id


def build_motor_position_row(positions: dict[str, Any], field_name: str, scale: int) -> list[int]:
    values: list[int] = []
    for position_key in MOTOR_POSITION_KEYS:
        position = positions.get(position_key)
        if not isinstance(position, dict):
            raise ValueError(f"Motor_Cfg.positions 缺少位置 {position_key!r}。")
        values.append(scale_motor_numeric(position.get(field_name), scale, f"positions.{position_key}.{field_name}"))
    return values


def build_motor_afs_rows(afs_positions: dict[str, Any]) -> list[list[int]]:
    rows: list[list[int]] = []
    for level_key in MOTOR_AFS_LEVEL_KEYS:
        level = afs_positions.get(level_key)
        if not isinstance(level, dict):
            raise ValueError(f"Motor_Cfg.afs_positions 缺少档位 {level_key!r}。")
        rows.append(
            [
                scale_motor_numeric(level.get("c_mode"), 100, f"afs_positions.{level_key}.c_mode"),
                scale_motor_numeric(level.get("v_mode"), 100, f"afs_positions.{level_key}.v_mode"),
                scale_motor_numeric(level.get("e_mode"), 100, f"afs_positions.{level_key}.e_mode"),
            ]
        )
    return rows


def build_motor_run_rows(control_modes: dict[str, Any]) -> list[tuple[str, list[int]]]:
    rows: list[tuple[str, list[int]]] = []
    for mode_key, comment in MOTOR_RUN_MODE_KEY_MAP:
        mode = control_modes.get(mode_key)
        if not isinstance(mode, dict):
            raise ValueError(f"Motor_Cfg.control_modes 缺少模式 {mode_key!r}。")
        rows.append(
            (
                comment,
                [
                    scale_motor_numeric(mode.get(field_name), 1, f"control_modes.{mode_key}.{field_name}")
                    for field_name in MOTOR_RUN_FIELD_KEYS
                ],
            )
        )
    return rows


def build_motor_dc_level_values(items_by_id: dict[str, Any]) -> list[int]:
    item = items_by_id.get(str(MOTOR_DC_LEVEL_CFG_ID))
    if not isinstance(item, dict):
        raise ValueError("HCM_PriLIN_Matrix.json 缺少 CFG 项 17，无法生成 dc_motor_level_info。")

    entries = item.get("entries")
    if not isinstance(entries, list):
        raise ValueError("CFG 项 17 缺少 entries，无法生成 dc_motor_level_info。")

    levels_by_index: dict[int, int] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("CFG 项 17 存在无效 entry，无法生成 dc_motor_level_info。")
        raw_index = entry.get("value_1")
        if isinstance(raw_index, bool) or not isinstance(raw_index, int):
            raise ValueError("CFG 项 17 的 value_1 必须是整数档位索引。")
        levels_by_index[raw_index] = scale_motor_numeric(entry.get("value_2"), 100, f"CHCM[17].value_2[{raw_index}]")

    expected_indexes = range(4)
    missing_indexes = [index for index in expected_indexes if index not in levels_by_index]
    if missing_indexes:
        raise ValueError(f"CFG 项 17 缺少档位 {missing_indexes}，无法生成 dc_motor_level_info。")
    return [levels_by_index[index] for index in expected_indexes]


def build_motor_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    motor_placeholder_required = any(name.startswith("MOTOR_") for name in required_placeholders)
    if not motor_placeholder_required:
        return {}

    motor_config, items_by_id = load_motor_config_sources(excel_payloads)

    safety_voltage = require_dict(motor_config, "safety_voltage", "Motor_Cfg.motor_config")
    general_settings = require_dict(motor_config, "general_settings", "Motor_Cfg.motor_config")
    control_modes = require_dict(motor_config, "control_modes", "Motor_Cfg.motor_config")
    positions = require_dict(motor_config, "positions", "Motor_Cfg.motor_config")
    afs_positions = require_dict(motor_config, "afs_positions", "Motor_Cfg.motor_config")

    motor_low_voltage = scale_motor_numeric(safety_voltage.get("low_voltage_v"), 10, "safety_voltage.low_voltage_v")
    motor_over_voltage = scale_motor_numeric(safety_voltage.get("over_voltage_v"), 10, "safety_voltage.over_voltage_v")
    motor_direction = resolve_motor_direction_macro(general_settings.get("positive_command_action"))
    motor_full_step_per_mm = scale_motor_numeric(general_settings.get("full_steps_per_mm"), 100, "general_settings.full_steps_per_mm")
    motor_wall_ratio = scale_motor_numeric(
        general_settings.get("wall_command_ratio_per_mm_at_10m"),
        100,
        "general_settings.wall_command_ratio_per_mm_at_10m",
    )

    position_steps = build_motor_position_row(positions, "steps_to_pos1_fs", 100)
    position_distances = build_motor_position_row(positions, "spindle_distance_to_pos1_mm", 100)
    position_wall_values = build_motor_position_row(positions, "wall_position_mm", 1)
    position_angles = build_motor_position_row(positions, "angle_deg", 100)
    motor_run_rows = build_motor_run_rows(control_modes)
    motor_step_mode = resolve_motor_step_mode_macro(motor_config.get("microstep_mode"))
    motor_afs_rows = build_motor_afs_rows(afs_positions)
    dc_motor_level_values = build_motor_dc_level_values(items_by_id)
    run_rows_by_mode = {
        mode_key: values
        for (mode_key, _comment), (_comment2, values) in zip(MOTOR_RUN_MODE_KEY_MAP, motor_run_rows, strict=True)
    }

    placeholders: dict[str, Any] = {
        "MOTOR_LOW_VOLTAGE": motor_low_voltage,
        "MOTOR_OVER_VOLTAGE": motor_over_voltage,
        "MOTOR_DIRECTION": motor_direction,
        "MOTOR_FULL_STEP_1MM": motor_full_step_per_mm,
        "MOTOR_DISTANCE_RATIO_1MM": motor_wall_ratio,
        "MOTOR_STEP_MODE": motor_step_mode,
    }

    for index, value in enumerate(position_steps, start=1):
        placeholders[f"MOTOR_POSITION_POS{index}_STEP_TO_POS"] = value
    for index, value in enumerate(position_distances, start=1):
        placeholders[f"MOTOR_POSITION_POS{index}_DISTANCE_TO_POS"] = value
    for index, value in enumerate(position_wall_values, start=1):
        placeholders[f"MOTOR_POSITION_POS{index}_WALL_POS"] = value
    for index, value in enumerate(position_angles, start=1):
        placeholders[f"MOTOR_POSITION_POS{index}_ANGLE"] = value

    for mode_key, values in run_rows_by_mode.items():
        mode_prefix = "MOTOR_REFERENCE_RUN" if mode_key == "reference_run" else "MOTOR_NORMAL_RUN"
        for field_name, value in zip(MOTOR_RUN_FIELD_KEYS, values, strict=True):
            field_suffix = {
                "running_current": "RUNNING_CURRENT",
                "holding_current": "HOLDING_CURRENT",
                "max_acceleration_ramp": "ACCELERATION",
                "min_speed": "MIN_SPEED",
                "normal_speed": "NORMAL_SPEED",
                "max_speed": "MAX_SPEED",
            }[field_name]
            placeholders[f"{mode_prefix}_{field_suffix}"] = value

    for level_index, values in enumerate(motor_afs_rows):
        placeholders[f"MOTOR_AFS_LEVEL{level_index}_C_MODE"] = values[0]
        placeholders[f"MOTOR_AFS_LEVEL{level_index}_V_MODE"] = values[1]
        placeholders[f"MOTOR_AFS_LEVEL{level_index}_E_MODE"] = values[2]

    for level_index, value in enumerate(dc_motor_level_values):
        placeholders[f"MOTOR_DC_LEVEL{level_index}"] = value

    return placeholders


def build_render_context(
    excel_payloads: dict[str, dict[str, Any]],
    kconfig_payload: dict[str, Any],
    required_placeholders: set[str],
) -> dict[str, Any]:
    placeholders = {**SCALAR_DEFAULTS, **extract_scalar_placeholders(kconfig_payload, excel_payloads)}
    sections: dict[str, str] = {}
    placeholders.update(build_cvcc_output_voltage_placeholders(kconfig_payload, required_placeholders))
    placeholders.update(build_chcm_cfg_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_motor_placeholders(excel_payloads, required_placeholders))

    for name in sorted(required_placeholders):
        if is_block_placeholder(name):
            sections.setdefault(name, build_section_stub(name, excel_payloads))
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

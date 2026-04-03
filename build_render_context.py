from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


INPUT_DIR_DEFAULT = Path("output")
KCONFIG_JSON_DEFAULT = INPUT_DIR_DEFAULT / "Kconfig.json"
OUTPUT_DEFAULT = INPUT_DIR_DEFAULT / "render_context.json"
HEADER_TEMPLATE_DEFAULT = Path("templates") / "app_config.h.tpl"
SOURCE_TEMPLATE_DEFAULT = Path("templates") / "app_config.c.tpl"
ANIMATION_BOARD_TYPE_MAP_DEFAULT = Path("animation_board_type_map.json")
OUTPUT_SCHEMA_VERSION = 1
PLACEHOLDER_PATTERN = re.compile(r"@([A-Z0-9_]+)@")
BLOCK_PLACEHOLDER_TOKENS = ("DEFINITION", "DEFINITIONS", "DECLARATION", "DECLARATIONS", "MACRO", "MACROS")
SCALAR_DEFAULTS = {
    "PROJECT_NAME": "PROJECT_A_SMALL",
    "SYSTEM_COM_VERION": "VERSION_V5",
    "EEA_X": "VERSION_V5",
    "HB_LB_ANIMATION_ENABLE": 0,
    "CVCC_IC_TYPE": "CVCC_NSL20912",
    "CVCC_UART_CHANNEL": "SUB_UARTCAN_1",
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
    "CH_CFG_TYPE0_CVCC_MAP_ARRAY_SIZE": 1,
    "CH_CFG_TYPE0_CVCC_MAP_NUMS": 0,
    "CH_CFG_TYPE1_CVCC_MAP_ARRAY_SIZE": 1,
    "CH_CFG_TYPE1_CVCC_MAP_NUMS": 0,
    "CH_CFG_TYPE2_CVCC_MAP_ARRAY_SIZE": 1,
    "CH_CFG_TYPE2_CVCC_MAP_NUMS": 0,
    "CH_CFG_TYPE3_CVCC_MAP_ARRAY_SIZE": 1,
    "CH_CFG_TYPE3_CVCC_MAP_NUMS": 0,
    "CH_CFG_TYPE4_CVCC_MAP_ARRAY_SIZE": 1,
    "CH_CFG_TYPE4_CVCC_MAP_NUMS": 0,
    "CH_CFG_TYPE5_CVCC_MAP_ARRAY_SIZE": 1,
    "CH_CFG_TYPE5_CVCC_MAP_NUMS": 0,
    "CH_CFG_TYPE6_CVCC_MAP_ARRAY_SIZE": 1,
    "CH_CFG_TYPE6_CVCC_MAP_NUMS": 0,
    "CH_CFG_TYPE7_CVCC_MAP_ARRAY_SIZE": 1,
    "CH_CFG_TYPE7_CVCC_MAP_NUMS": 0,
    "CH_CFG_TYPE8_CVCC_MAP_ARRAY_SIZE": 1,
    "CH_CFG_TYPE8_CVCC_MAP_NUMS": 0,
    "CH_CFG_TYPE8_FIXED_CURRENT": 0,
    "CH_CFG_TYPE9_CVCC_MAP_ARRAY_SIZE": 1,
    "CH_CFG_TYPE9_CVCC_MAP_NUMS": 0,
    "CH_CFG_TYPE9_FIXED_CURRENT": 0,
    "CH_CFG_TYPE0_UNLOCK_LOCK_OFFSET": 255,
    "CH_CFG_TYPE2_UNLOCK_LOCK_OFFSET": 255,
    "CH_CFG_TYPE3_UNLOCK_LOCK_OFFSET": 255,
    "CH_CFG_TYPE4_UNLOCK_LOCK_OFFSET": 255,
    "CH_CFG_TYPE5_UNLOCK_LOCK_OFFSET": 255,
    "CH_CFG_TYPE6_UNLOCK_LOCK_OFFSET": 255,
    "CH_CFG_TYPE7_UNLOCK_LOCK_OFFSET": 255,
    "CH_CFG_TYPE8_UNLOCK_LOCK_OFFSET": 255,
    "PL_0_UNLOCK_LOCK_OFFSET": 255,
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
CVCC_CFG_IC_ADDR_INDEXES = tuple(range(12))
CVCC_CFG_UNUSED_IC_ADDR = 255
CVCC_K_ARRAY_FIXED_IC_COUNT = 12
CVCC_K_ARRAY_FIXED_CHANNEL_COUNT = 24
CH_CFG_CONFIG_TYPE_IDS = tuple(range(10))
ANIMATION_CFG_KIND_NAMES = ("lock", "unlock")
ANIMATION_CFG_MAX_MODE_COUNT = 5
RAW_SIGNAL_ANIMATION_SHEET_PATTERN = re.compile(r"^(lock|unlock)\s+mode\s*(\d+)$", re.IGNORECASE)
ANSI_RED = "\033[31m"
ANSI_BOLD = "\033[1m"
ANSI_RESET = "\033[0m"
TI_SEQUENTIAL_CHANNEL_PATTERN = re.compile(r"^IC(\d+)-CH(\d+)$")
CVCC_IC_TYPE_SYMBOL_TO_MACRO = {
    "CVCC_IC_TYPE_TPS929120": "CVCC_TPS929120",
    "CVCC_IC_TYPE_TPS929160": "CVCC_TPS929160",
    "CVCC_IC_TYPE_TPS929240": "CVCC_TPS929240",
    "CVCC_IC_TYPE_NSL20912": "CVCC_NSL20912",
}
CVCC_UART_CHANNEL_SYMBOL_TO_MACRO = {
    "CVCC_UART_UARTCAN_0": "SUB_UARTCAN_0",
    "CVCC_UART_UARTCAN_1": "SUB_UARTCAN_1",
    "CVCC_UART_UARTCAN_2": "SUB_UARTCAN_2",
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


def extract_current_config_channel_counts(current_config_payload: dict[str, Any]) -> dict[str, int]:
    channels = collect_current_config_effective_channels(current_config_payload)
    if not channels:
        return {}

    ti_led_nums = 0

    for channel_payload in channels.values():
        if not isinstance(channel_payload, dict):
            continue

        function_names: set[str] = set()
        for function_key in ("primary_function", "secondary_function"):
            function_payload = channel_payload.get(function_key)
            if not isinstance(function_payload, dict):
                continue
            function_name = function_payload.get("name")
            if isinstance(function_name, str) and function_name:
                function_names.add(function_name)

        if "TI" in function_names:
            ti_led_nums += 1

    return {
        "TI_USED_LED_NUMS": ti_led_nums,
        "TI_USED_LED_NUMS_DATA_LENS": math.ceil(ti_led_nums / 32) if ti_led_nums else 0,
    }


def collect_current_config_effective_channels(current_config_payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    channels = current_config_payload.get("channels")
    if not isinstance(channels, dict):
        return {}

    effective_channels: dict[str, dict[str, Any]] = {}
    for channel_key, channel_payload in channels.items():
        if not isinstance(channel_payload, dict):
            continue
        if any(field in channel_payload for field in ("primary_function", "secondary_function", "fixed_current")):
            effective_channels[str(channel_key)] = channel_payload
    return effective_channels


def collect_ch_cfg_channel_types(ch_cfg_payload: dict[str, Any]) -> dict[str, int]:
    ic_payloads = require_dict(ch_cfg_payload, "ics", "CH_Cfg.json")
    channel_types: dict[str, int] = {}

    for ic_name, channels in ic_payloads.items():
        if not isinstance(channels, dict):
            raise ValueError(f"CH_Cfg.json 的 {ic_name} 不是对象。")
        for channel_name, config_type in channels.items():
            if isinstance(config_type, bool) or not isinstance(config_type, int):
                raise ValueError(f"CH_Cfg.json 的 {ic_name}-{channel_name} 通道类型无效。")
            channel_key = f"{ic_name}-{channel_name}"
            channel_types[channel_key] = config_type

    return channel_types


def format_channel_key_list(channel_keys: set[str], *, limit: int = 20) -> str:
    if not channel_keys:
        return "无"

    ordered_keys = sorted(channel_keys)
    if len(ordered_keys) <= limit:
        return ", ".join(ordered_keys)
    preview = ", ".join(ordered_keys[:limit])
    return f"{preview} ... 共 {len(ordered_keys)} 个"


def format_type_mismatch_summary(
    ch_cfg_channel_types: dict[str, int],
    current_channel_keys: set[str],
    descriptions: dict[str, str],
) -> str:
    ch_cfg_counts = {str(config_type): 0 for config_type in CH_CFG_CONFIG_TYPE_IDS}
    current_counts = {str(config_type): 0 for config_type in CH_CFG_CONFIG_TYPE_IDS}

    for channel_key, config_type in ch_cfg_channel_types.items():
        config_type_key = str(config_type)
        if config_type_key not in ch_cfg_counts:
            continue
        ch_cfg_counts[config_type_key] += 1
        if channel_key in current_channel_keys:
            current_counts[config_type_key] += 1

    mismatch_lines = []
    for config_type_key in ch_cfg_counts:
        if ch_cfg_counts[config_type_key] == current_counts[config_type_key]:
            continue
        description = descriptions.get(config_type_key, "")
        label = f"type {config_type_key}"
        if description:
            label += f"({description})"
        mismatch_lines.append(
            f"{label}: CH_Cfg={ch_cfg_counts[config_type_key]}, current_config={current_counts[config_type_key]}"
        )

    return "；".join(mismatch_lines) if mismatch_lines else "无"


def validate_channel_config_consistency(excel_payloads: dict[str, dict[str, Any]]) -> tuple[dict[str, int], dict[str, dict[str, Any]]]:
    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="校验通道配置一致性")
    current_config_payload = require_excel_payload(excel_payloads, "current_config", purpose="校验通道配置一致性")
    descriptions = ch_cfg_payload.get("config_type_descriptions")
    if not isinstance(descriptions, dict):
        raise ValueError("CH_Cfg.json 缺少 config_type_descriptions。")

    ch_cfg_channel_types = collect_ch_cfg_channel_types(ch_cfg_payload)
    current_effective_channels = collect_current_config_effective_channels(current_config_payload)

    current_channel_keys = set(current_effective_channels)
    mismatch_summary = format_type_mismatch_summary(ch_cfg_channel_types, current_channel_keys, descriptions)
    if mismatch_summary != "无":
        raise ValueError(
            "CH_Cfg.json 与 current_config.json 的通道类型数量不一致，请检查 Excel 配置是否有误。"
            f" {mismatch_summary}。"
        )

    return ch_cfg_channel_types, current_effective_channels


def build_ch_cfg_channel_counts_domain(excel_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="统计 CH_Cfg 通道类型数量")
    descriptions = ch_cfg_payload.get("config_type_descriptions")
    if not isinstance(descriptions, dict):
        raise ValueError("CH_Cfg.json 缺少 config_type_descriptions。")

    counts = {str(config_type): 0 for config_type in CH_CFG_CONFIG_TYPE_IDS}
    for channel_key, config_type in collect_ch_cfg_channel_types(ch_cfg_payload).items():
        config_type_key = str(config_type)
        if config_type_key not in counts:
            raise ValueError(f"CH_Cfg.json 的 {channel_key} 出现未支持的通道类型 {config_type}。")
        counts[config_type_key] += 1

    by_type = {
        config_type_key: {
            "description": descriptions.get(config_type_key, ""),
            "count": counts[config_type_key],
        }
        for config_type_key in counts
    }

    return {
        "total_channels": sum(counts.values()),
        "channel_count": ch_cfg_payload.get("channel_count", sum(counts.values())),
        "by_type": by_type,
    }


def build_ch_cfg_fixed_currents_domain(
    excel_payloads: dict[str, dict[str, Any]],
    ch_cfg_channel_types: dict[str, int],
    current_effective_channels: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="统计 CH_Cfg 固定电流")
    descriptions = ch_cfg_payload.get("config_type_descriptions")
    if not isinstance(descriptions, dict):
        raise ValueError("CH_Cfg.json 缺少 config_type_descriptions。")

    channels_by_type: dict[str, list[str]] = {str(config_type): [] for config_type in CH_CFG_CONFIG_TYPE_IDS}
    for channel_key, config_type in sorted(ch_cfg_channel_types.items()):
        config_type_key = str(config_type)
        if config_type_key not in channels_by_type:
            raise ValueError(f"CH_Cfg.json 的 {channel_key} 出现未支持的通道类型 {config_type}。")
        channels_by_type[config_type_key].append(channel_key)

    by_type: dict[str, Any] = {}
    for config_type_key in channels_by_type:
        channel_keys = channels_by_type[config_type_key]
        fixed_current_values: set[int] = set()
        missing_fixed_current_channels: list[str] = []
        fixed_current_channel_count = 0

        for channel_key in channel_keys:
            channel_payload = current_effective_channels.get(channel_key)
            if channel_payload is None:
                raise ValueError(f"current_config.json 缺少通道 {channel_key}，请检查 Excel 配置是否有误。")

            fixed_current = channel_payload.get("fixed_current")
            if fixed_current is None:
                continue
            if isinstance(fixed_current, bool) or not isinstance(fixed_current, int):
                raise ValueError(f"current_config.json 中 {channel_key}.fixed_current 必须是整数。")
            fixed_current_values.add(fixed_current)
            fixed_current_channel_count += 1

        if fixed_current_channel_count:
            for channel_key in channel_keys:
                channel_payload = current_effective_channels[channel_key]
                if channel_payload.get("fixed_current") is None:
                    missing_fixed_current_channels.append(channel_key)

        if missing_fixed_current_channels:
            raise ValueError(
                f"type {config_type_key} 的 fixed_current 配置不完整，缺少通道: "
                f"{format_channel_key_list(set(missing_fixed_current_channels), limit=len(missing_fixed_current_channels))}。"
            )
        if len(fixed_current_values) > 1:
            values = ", ".join(str(value) for value in sorted(fixed_current_values))
            raise ValueError(f"type {config_type_key} 的 fixed_current 不唯一: {values}。")

        by_type[config_type_key] = {
            "description": descriptions.get(config_type_key, ""),
            "channel_count": len(channel_keys),
            "fixed_current_channel_count": fixed_current_channel_count,
            "fixed_current": next(iter(fixed_current_values)) if fixed_current_values else None,
            "channels": channel_keys,
        }

    return {
        "by_type": by_type,
    }


def build_ch_cfg_fixed_current_placeholders(
    ch_cfg_fixed_currents: dict[str, Any],
    required_placeholders: set[str],
) -> dict[str, Any]:
    placeholder_map = {
        "CH_CFG_TYPE8_FIXED_CURRENT": "8",
        "CH_CFG_TYPE9_FIXED_CURRENT": "9",
    }
    required_map = {
        placeholder_name: type_key
        for placeholder_name, type_key in placeholder_map.items()
        if placeholder_name in required_placeholders
    }
    if not required_map:
        return {}

    by_type = ch_cfg_fixed_currents.get("by_type")
    if not isinstance(by_type, dict):
        raise ValueError("ch_cfg_fixed_currents 缺少 by_type。")

    placeholders: dict[str, Any] = {}
    for placeholder_name, type_key in required_map.items():
        type_payload = by_type.get(type_key)
        if not isinstance(type_payload, dict):
            raise ValueError(f"ch_cfg_fixed_currents 缺少 type {type_key} 固定电流配置。")

        fixed_current = type_payload.get("fixed_current")
        if isinstance(fixed_current, bool) or not isinstance(fixed_current, int):
            raise ValueError(f"type {type_key} 的 fixed_current 无效，无法生成 {placeholder_name}。")
        placeholders[placeholder_name] = fixed_current

    return placeholders


def parse_ch_cfg_index(name: str, prefix: str) -> int:
    if not isinstance(name, str) or not name.startswith(prefix):
        raise ValueError(f"CH_Cfg.json 存在无效键 {name!r}。")
    try:
        return int(name[len(prefix):])
    except ValueError as exc:
        raise ValueError(f"CH_Cfg.json 存在无效键 {name!r}。") from exc


def format_ch_cfg_type0_rows(entries: list[tuple[int, int]]) -> str:
    if not entries:
        return "    /* UNUSED */"

    lines = [
        f"    {{ {ic_index:2d}U, {channel_index:2d}U }}, /**< {entry_index:2d} - IC{ic_index}-CH{channel_index:02d} */"
        for entry_index, (ic_index, channel_index) in enumerate(entries, start=1)
    ]
    return "\n".join(lines)


def build_ch_cfg_type0_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    placeholder_names = {
        "CH_CFG_TYPE0_CVCC_MAP_ARRAY_SIZE",
        "CH_CFG_TYPE0_CVCC_MAP_ROWS",
        "CH_CFG_TYPE0_CVCC_MAP_NUMS",
    }
    if not any(name in required_placeholders for name in placeholder_names):
        return {}

    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="生成 CH_Cfg type0 通道映射占位符")
    ic_payloads = require_dict(ch_cfg_payload, "ics", "CH_Cfg.json")

    type0_entries: list[tuple[int, int]] = []
    for ic_name, channels in sorted(
        ic_payloads.items(),
        key=lambda item: parse_ch_cfg_index(item[0], "IC"),
    ):
        if not isinstance(channels, dict):
            raise ValueError(f"CH_Cfg.json 的 {ic_name} 不是对象。")
        ic_index = parse_ch_cfg_index(ic_name, "IC")
        for channel_name, config_type in sorted(
            channels.items(),
            key=lambda item: parse_ch_cfg_index(item[0], "CH"),
        ):
            if config_type != 0:
                continue
            channel_index = parse_ch_cfg_index(channel_name, "CH")
            type0_entries.append((ic_index, channel_index))

    type0_count = len(type0_entries)
    return {
        "CH_CFG_TYPE0_CVCC_MAP_ARRAY_SIZE": type0_count if type0_count else 1,
        "CH_CFG_TYPE0_CVCC_MAP_ROWS": format_ch_cfg_type0_rows(type0_entries),
        "CH_CFG_TYPE0_CVCC_MAP_NUMS": type0_count,
    }


def build_ch_cfg_type1_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    placeholder_names = {
        "CH_CFG_TYPE1_CVCC_MAP_ARRAY_SIZE",
        "CH_CFG_TYPE1_CVCC_MAP_ROWS",
        "CH_CFG_TYPE1_CVCC_MAP_NUMS",
    }
    if not any(name in required_placeholders for name in placeholder_names):
        return {}

    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="生成 CH_Cfg type1 通道映射占位符")
    ic_payloads = require_dict(ch_cfg_payload, "ics", "CH_Cfg.json")

    type1_entries: list[tuple[int, int]] = []
    for ic_name, channels in sorted(
        ic_payloads.items(),
        key=lambda item: parse_ch_cfg_index(item[0], "IC"),
        reverse=True,
    ):
        if not isinstance(channels, dict):
            raise ValueError(f"CH_Cfg.json 的 {ic_name} 不是对象。")
        ic_index = parse_ch_cfg_index(ic_name, "IC")
        for channel_name, config_type in sorted(
            channels.items(),
            key=lambda item: parse_ch_cfg_index(item[0], "CH"),
            reverse=True,
        ):
            if config_type != 1:
                continue
            channel_index = parse_ch_cfg_index(channel_name, "CH")
            type1_entries.append((ic_index, channel_index))

    type1_count = len(type1_entries)
    if not type1_entries:
        rows = "    /* UNUSED */"
    else:
        rows = "\n".join(
            (
                f"    {{ {ic_index:2d}U, {channel_index:2d}U }}, "
                f"/**< {entry_index:2d} - TI_{((type1_count - entry_index) // 2) + 1:02d} */"
            )
            for entry_index, (ic_index, channel_index) in enumerate(type1_entries, start=1)
        )

    return {
        "CH_CFG_TYPE1_CVCC_MAP_ARRAY_SIZE": type1_count if type1_count else 1,
        "CH_CFG_TYPE1_CVCC_MAP_ROWS": rows,
        "CH_CFG_TYPE1_CVCC_MAP_NUMS": type1_count,
    }


def build_ch_cfg_type2_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    placeholder_names = {
        "CH_CFG_TYPE2_CVCC_MAP_ARRAY_SIZE",
        "CH_CFG_TYPE2_CVCC_MAP_ROWS",
        "CH_CFG_TYPE2_CVCC_MAP_NUMS",
    }
    if not any(name in required_placeholders for name in placeholder_names):
        return {}

    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="生成 CH_Cfg type2 通道映射占位符")
    ic_payloads = require_dict(ch_cfg_payload, "ics", "CH_Cfg.json")

    type2_entries: list[tuple[int, int]] = []
    for ic_name, channels in sorted(
        ic_payloads.items(),
        key=lambda item: parse_ch_cfg_index(item[0], "IC"),
        reverse=True,
    ):
        if not isinstance(channels, dict):
            raise ValueError(f"CH_Cfg.json 的 {ic_name} 不是对象。")
        ic_index = parse_ch_cfg_index(ic_name, "IC")
        for channel_name, config_type in sorted(
            channels.items(),
            key=lambda item: parse_ch_cfg_index(item[0], "CH"),
            reverse=True,
        ):
            if config_type != 2:
                continue
            channel_index = parse_ch_cfg_index(channel_name, "CH")
            type2_entries.append((ic_index, channel_index))

    type2_count = len(type2_entries)
    if not type2_entries:
        rows = "    /* UNUSED */"
    else:
        rows = "\n".join(
            f"    {{ {ic_index:2d}U, {channel_index:2d}U }}, /**< {entry_index:2d} - DRL_POS_{type2_count - entry_index + 1:02d} */"
            for entry_index, (ic_index, channel_index) in enumerate(type2_entries, start=1)
        )

    return {
        "CH_CFG_TYPE2_CVCC_MAP_ARRAY_SIZE": type2_count if type2_count else 1,
        "CH_CFG_TYPE2_CVCC_MAP_ROWS": rows,
        "CH_CFG_TYPE2_CVCC_MAP_NUMS": type2_count,
    }


def build_ch_cfg_type3_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    placeholder_names = {
        "CH_CFG_TYPE3_CVCC_MAP_ARRAY_SIZE",
        "CH_CFG_TYPE3_CVCC_MAP_ROWS",
        "CH_CFG_TYPE3_CVCC_MAP_NUMS",
    }
    if not any(name in required_placeholders for name in placeholder_names):
        return {}

    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="生成 CH_Cfg type3 通道映射占位符")
    ic_payloads = require_dict(ch_cfg_payload, "ics", "CH_Cfg.json")

    type3_entries: list[tuple[int, int]] = []
    for ic_name, channels in sorted(
        ic_payloads.items(),
        key=lambda item: parse_ch_cfg_index(item[0], "IC"),
        reverse=True,
    ):
        if not isinstance(channels, dict):
            raise ValueError(f"CH_Cfg.json 的 {ic_name} 不是对象。")
        ic_index = parse_ch_cfg_index(ic_name, "IC")
        for channel_name, config_type in sorted(
            channels.items(),
            key=lambda item: parse_ch_cfg_index(item[0], "CH"),
            reverse=True,
        ):
            if config_type != 3:
                continue
            channel_index = parse_ch_cfg_index(channel_name, "CH")
            type3_entries.append((ic_index, channel_index))

    type3_count = len(type3_entries)
    if not type3_entries:
        rows = "    /* UNUSED */"
    else:
        rows = "\n".join(
            f"    {{ {ic_index:2d}U, {channel_index:2d}U }}, /**< {entry_index:2d} - DRLPOS_{type3_count - entry_index + 1:02d} */"
            for entry_index, (ic_index, channel_index) in enumerate(type3_entries, start=1)
        )

    return {
        "CH_CFG_TYPE3_CVCC_MAP_ARRAY_SIZE": type3_count if type3_count else 1,
        "CH_CFG_TYPE3_CVCC_MAP_ROWS": rows,
        "CH_CFG_TYPE3_CVCC_MAP_NUMS": type3_count,
    }


def build_ch_cfg_type4_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    placeholder_names = {
        "CH_CFG_TYPE4_CVCC_MAP_ARRAY_SIZE",
        "CH_CFG_TYPE4_CVCC_MAP_ROWS",
        "CH_CFG_TYPE4_CVCC_MAP_NUMS",
    }
    if not any(name in required_placeholders for name in placeholder_names):
        return {}

    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="生成 CH_Cfg type4 通道映射占位符")
    ic_payloads = require_dict(ch_cfg_payload, "ics", "CH_Cfg.json")

    type4_entries: list[tuple[int, int]] = []
    for ic_name, channels in sorted(
        ic_payloads.items(),
        key=lambda item: parse_ch_cfg_index(item[0], "IC"),
        reverse=True,
    ):
        if not isinstance(channels, dict):
            raise ValueError(f"CH_Cfg.json 的 {ic_name} 不是对象。")
        ic_index = parse_ch_cfg_index(ic_name, "IC")
        for channel_name, config_type in sorted(
            channels.items(),
            key=lambda item: parse_ch_cfg_index(item[0], "CH"),
            reverse=True,
        ):
            if config_type != 4:
                continue
            channel_index = parse_ch_cfg_index(channel_name, "CH")
            type4_entries.append((ic_index, channel_index))

    type4_count = len(type4_entries)
    if not type4_entries:
        rows = "    /* UNUSED */"
    else:
        rows = "\n".join(
            f"    {{ {ic_index:2d}U, {channel_index:2d}U }}, /**< {entry_index:2d} - DRLPL_{type4_count - entry_index + 1:02d} */"
            for entry_index, (ic_index, channel_index) in enumerate(type4_entries, start=1)
        )

    return {
        "CH_CFG_TYPE4_CVCC_MAP_ARRAY_SIZE": type4_count if type4_count else 1,
        "CH_CFG_TYPE4_CVCC_MAP_ROWS": rows,
        "CH_CFG_TYPE4_CVCC_MAP_NUMS": type4_count,
    }


def build_ch_cfg_drl_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
    *,
    config_type: int,
    array_size_name: str,
    rows_name: str,
    nums_name: str,
) -> dict[str, Any]:
    placeholder_names = {array_size_name, rows_name, nums_name}
    if not any(name in required_placeholders for name in placeholder_names):
        return {}

    ch_cfg_payload = require_excel_payload(
        excel_payloads,
        "CH_Cfg",
        purpose=f"生成 CH_Cfg type{config_type} 通道映射占位符",
    )
    ic_payloads = require_dict(ch_cfg_payload, "ics", "CH_Cfg.json")

    entries: list[tuple[int, int]] = []
    for ic_name, channels in sorted(
        ic_payloads.items(),
        key=lambda item: parse_ch_cfg_index(item[0], "IC"),
        reverse=True,
    ):
        if not isinstance(channels, dict):
            raise ValueError(f"CH_Cfg.json 的 {ic_name} 不是对象。")
        ic_index = parse_ch_cfg_index(ic_name, "IC")
        for channel_name, channel_config_type in sorted(
            channels.items(),
            key=lambda item: parse_ch_cfg_index(item[0], "CH"),
            reverse=True,
        ):
            if channel_config_type != config_type:
                continue
            channel_index = parse_ch_cfg_index(channel_name, "CH")
            entries.append((ic_index, channel_index))

    entry_count = len(entries)
    if not entries:
        rows = "    /* UNUSED */"
    else:
        rows = "\n".join(
            f"    {{ {ic_index:2d}U, {channel_index:2d}U }}, /**< {entry_index:2d} - DRL_{entry_count - entry_index + 1:02d} */"
            for entry_index, (ic_index, channel_index) in enumerate(entries, start=1)
        )

    return {
        array_size_name: entry_count if entry_count else 1,
        rows_name: rows,
        nums_name: entry_count,
    }


def build_ch_cfg_type5_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    return build_ch_cfg_drl_placeholders(
        excel_payloads,
        required_placeholders,
        config_type=5,
        array_size_name="CH_CFG_TYPE5_CVCC_MAP_ARRAY_SIZE",
        rows_name="CH_CFG_TYPE5_CVCC_MAP_ROWS",
        nums_name="CH_CFG_TYPE5_CVCC_MAP_NUMS",
    )


def build_ch_cfg_type6_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    return build_ch_cfg_drl_placeholders(
        excel_payloads,
        required_placeholders,
        config_type=6,
        array_size_name="CH_CFG_TYPE6_CVCC_MAP_ARRAY_SIZE",
        rows_name="CH_CFG_TYPE6_CVCC_MAP_ROWS",
        nums_name="CH_CFG_TYPE6_CVCC_MAP_NUMS",
    )


def build_ch_cfg_type7_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    return build_ch_cfg_drl_placeholders(
        excel_payloads,
        required_placeholders,
        config_type=7,
        array_size_name="CH_CFG_TYPE7_CVCC_MAP_ARRAY_SIZE",
        rows_name="CH_CFG_TYPE7_CVCC_MAP_ROWS",
        nums_name="CH_CFG_TYPE7_CVCC_MAP_NUMS",
    )


def build_ch_cfg_type8_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    placeholder_names = {
        "CH_CFG_TYPE8_CVCC_MAP_ARRAY_SIZE",
        "CH_CFG_TYPE8_CVCC_MAP_ROWS",
        "CH_CFG_TYPE8_CVCC_MAP_NUMS",
    }
    if not any(name in required_placeholders for name in placeholder_names):
        return {}

    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="生成 CH_Cfg type8 通道映射占位符")
    ic_payloads = require_dict(ch_cfg_payload, "ics", "CH_Cfg.json")

    type8_entries: list[tuple[int, int]] = []
    for ic_name, channels in sorted(
        ic_payloads.items(),
        key=lambda item: parse_ch_cfg_index(item[0], "IC"),
    ):
        if not isinstance(channels, dict):
            raise ValueError(f"CH_Cfg.json 的 {ic_name} 不是对象。")
        ic_index = parse_ch_cfg_index(ic_name, "IC")
        for channel_name, config_type in sorted(
            channels.items(),
            key=lambda item: parse_ch_cfg_index(item[0], "CH"),
        ):
            if config_type != 8:
                continue
            channel_index = parse_ch_cfg_index(channel_name, "CH")
            type8_entries.append((ic_index, channel_index))

    type8_count = len(type8_entries)
    if not type8_entries:
        rows = "    /* UNUSED */"
    else:
        rows = "\n".join(
            f"    {{ {ic_index:2d}U, {channel_index:2d}U }}, /**< {entry_index:2d} - PL_{entry_index:02d} */"
            for entry_index, (ic_index, channel_index) in enumerate(type8_entries, start=1)
        )

    return {
        "CH_CFG_TYPE8_CVCC_MAP_ARRAY_SIZE": type8_count if type8_count else 1,
        "CH_CFG_TYPE8_CVCC_MAP_ROWS": rows,
        "CH_CFG_TYPE8_CVCC_MAP_NUMS": type8_count,
    }


def build_ch_cfg_type9_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, Any]:
    placeholder_names = {
        "CH_CFG_TYPE9_CVCC_MAP_ARRAY_SIZE",
        "CH_CFG_TYPE9_CVCC_MAP_ROWS",
        "CH_CFG_TYPE9_CVCC_MAP_NUMS",
    }
    if not any(name in required_placeholders for name in placeholder_names):
        return {}

    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="生成 CH_Cfg type9 通道映射占位符")
    ic_payloads = require_dict(ch_cfg_payload, "ics", "CH_Cfg.json")

    type9_entries: list[tuple[int, int]] = []
    for ic_name, channels in sorted(
        ic_payloads.items(),
        key=lambda item: parse_ch_cfg_index(item[0], "IC"),
        reverse=True,
    ):
        if not isinstance(channels, dict):
            raise ValueError(f"CH_Cfg.json 的 {ic_name} 不是对象。")
        ic_index = parse_ch_cfg_index(ic_name, "IC")
        for channel_name, config_type in sorted(
            channels.items(),
            key=lambda item: parse_ch_cfg_index(item[0], "CH"),
            reverse=True,
        ):
            if config_type != 9:
                continue
            channel_index = parse_ch_cfg_index(channel_name, "CH")
            type9_entries.append((ic_index, channel_index))

    type9_count = len(type9_entries)
    if not type9_entries:
        rows = "    /* UNUSED */"
    else:
        rows = "\n".join(
            f"    {{ {ic_index:2d}U, {channel_index:2d}U }}, /**< {entry_index:2d} - ADAS_{type9_count - entry_index + 1:02d} */"
            for entry_index, (ic_index, channel_index) in enumerate(type9_entries, start=1)
        )

    return {
        "CH_CFG_TYPE9_CVCC_MAP_ARRAY_SIZE": type9_count if type9_count else 1,
        "CH_CFG_TYPE9_CVCC_MAP_ROWS": rows,
        "CH_CFG_TYPE9_CVCC_MAP_NUMS": type9_count,
    }


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

    placeholders.update(extract_current_config_channel_counts(current_config))

    frames = ti_sequential.get("animation", {}).get("frames", [])
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


def active_kconfig_choice_symbol(symbols: dict[str, dict[str, Any]], names: tuple[str, ...]) -> str | None:
    for name in names:
        symbol = symbols.get(name)
        if isinstance(symbol, dict) and symbol.get("value") is True:
            return name
    return None


def resolve_kconfig_choice_macro(
    symbols: dict[str, dict[str, Any]],
    symbol_to_macro: dict[str, str],
    error_message: str,
) -> str:
    active_symbol = active_kconfig_choice_symbol(symbols, tuple(symbol_to_macro))
    if active_symbol is None:
        raise ValueError(error_message)
    return symbol_to_macro[active_symbol]


def format_cvcc_cfg_ic_addr_value(value: int) -> str:
    return f"{value:3d}"


def format_cvcc_cfg_used_switch_value(value: int) -> str:
    return f"{value:2d}"


def format_cvcc_cfg_max_current_value(value: int) -> str:
    return f"{value:2d}"


def parse_cvcc_cfg_channel_bit(channel_name: str) -> int:
    match = re.fullmatch(r"CH(\d+)", channel_name)
    if match is None:
        raise ValueError(f"CH_Cfg.json 中存在无效通道名 {channel_name!r}，无法生成 CVCC switch_mask。")

    bit_index = int(match.group(1))
    if bit_index >= 32:
        raise ValueError(f"CH_Cfg.json 中通道 {channel_name!r} 超出 uint32_t 掩码范围。")
    return bit_index


def format_cvcc_cfg_switch_mask_value(value: int) -> str:
    return f"0x{value:08x}"


def load_cvcc_cfg_excel_sources(
    excel_payloads: dict[str, dict[str, Any]]
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    ch_cfg_payload = require_excel_payload(excel_payloads, "CH_Cfg", purpose="生成 CVCC 配置占位符")
    ics = ch_cfg_payload.get("ics")
    if not isinstance(ics, dict):
        raise ValueError("CH_Cfg.json 缺少 ics，无法生成 CVCC 配置占位符。")

    current_config_payload = require_excel_payload(excel_payloads, "current_config", purpose="生成 CVCC 配置占位符")
    current_channels = current_config_payload.get("channels")
    if not isinstance(current_channels, dict):
        raise ValueError("current_config.json 缺少 channels，无法生成 CVCC 配置占位符。")

    return ics, current_channels


def resolve_cvcc_cfg_ic_max_current(
    ic_name: str,
    channel_names: tuple[str, ...],
    current_channels: dict[str, dict[str, Any]],
) -> int:
    max_currents: set[int] = set()
    for channel_name in channel_names:
        channel_key = f"{ic_name}-{channel_name}"
        channel_payload = current_channels.get(channel_key)
        if not isinstance(channel_payload, dict):
            raise ValueError(f"current_config.json 缺少通道 {channel_key}，无法生成 CVCC max_current。")

        max_current = channel_payload.get("max_current_per_channel")
        if max_current is None:
            continue
        if isinstance(max_current, bool) or not isinstance(max_current, int):
            raise ValueError(f"current_config.json 中 {channel_key}.max_current_per_channel 必须是整数。")
        max_currents.add(max_current)

    if not max_currents:
        if channel_names:
            raise ValueError(f"{ic_name} 在 CH_Cfg 中有使用通道，但 current_config 中缺少 max_current_per_channel。")
        return 0
    if len(max_currents) != 1:
        values = ", ".join(str(value) for value in sorted(max_currents))
        raise ValueError(f"{ic_name} 的 max_current_per_channel 不唯一: {values}")
    return next(iter(max_currents))


def coerce_cvcc_k_array_value(value: Any, channel_key: str) -> int:
    if value is None:
        return 100
    if isinstance(value, bool):
        raise ValueError(f"{channel_key}.primary_function.dimming_coefficient 不能是布尔值。")
    if isinstance(value, int):
        result = value
    elif isinstance(value, float):
        result = math.floor(value + 0.5)
    else:
        raise ValueError(f"{channel_key}.primary_function.dimming_coefficient 必须是数值。")

    if not 0 <= result <= 255:
        raise ValueError(f"{channel_key}.primary_function.dimming_coefficient 超出 uint8_t 范围: {result}")
    return result


def resolve_cvcc_k_array_channel_value(
    channel_key: str,
    current_channels: dict[str, dict[str, Any]],
) -> int:
    channel_payload = current_channels.get(channel_key)
    if not isinstance(channel_payload, dict):
        return 100

    primary_function = channel_payload.get("primary_function")
    if not isinstance(primary_function, dict):
        return 100
    return coerce_cvcc_k_array_value(primary_function.get("dimming_coefficient"), channel_key)


def format_cvcc_k_array_rows(rows: list[list[int]]) -> str:
    value_width = max((len(f"{value}U") for row in rows for value in row), default=len("100U"))
    lines: list[str] = []
    for row in rows:
        formatted_values = [f"{value}U".ljust(value_width) for value in row]
        lines.append(f"    {{ {', '.join(formatted_values)} }}, ")
    if lines:
        lines[-1] = lines[-1].removesuffix(", ")
    return "\n".join(lines)


def build_cvcc_cfg_domain(
    excel_payloads: dict[str, dict[str, Any]],
    kconfig_payload: dict[str, Any],
) -> dict[str, Any]:
    symbols = load_kconfig_symbols(kconfig_payload)
    ics, current_channels = load_cvcc_cfg_excel_sources(excel_payloads)

    cvcc_cfg_ics: dict[str, dict[str, Any]] = {}
    for ic_index in CVCC_CFG_IC_ADDR_INDEXES:
        ic_name = f"IC{ic_index}"
        channels = ics.get(ic_name)
        if not isinstance(channels, dict):
            raise ValueError(f"CH_Cfg.json 中 {ic_name} 不是对象，无法生成 CVCC 配置占位符。")

        channel_names = tuple(channels)
        used_switch = len(channel_names)
        switch_mask = 0
        for channel_name in channel_names:
            switch_mask |= 1 << parse_cvcc_cfg_channel_bit(channel_name)
        max_current = resolve_cvcc_cfg_ic_max_current(ic_name, channel_names, current_channels)
        ic_addr = ic_index if used_switch > 0 else CVCC_CFG_UNUSED_IC_ADDR

        cvcc_cfg_ics[ic_name] = {
            "addr": ic_addr,
            "used_switch": used_switch,
            "switch_mask": format_cvcc_cfg_switch_mask_value(switch_mask),
            "max_current": max_current,
        }

    k_array_rows: list[list[int]] = []
    for ic_index in range(CVCC_K_ARRAY_FIXED_IC_COUNT):
        row: list[int] = []
        for channel_index in range(CVCC_K_ARRAY_FIXED_CHANNEL_COUNT):
            channel_key = f"IC{ic_index}-CH{channel_index:02d}"
            row.append(resolve_cvcc_k_array_channel_value(channel_key, current_channels))
        k_array_rows.append(row)

    return {
        "ic_type": resolve_kconfig_choice_macro(
            symbols,
            CVCC_IC_TYPE_SYMBOL_TO_MACRO,
            "Kconfig 中未选择 CVCC IC Type，无法生成 CVCC 配置。",
        ),
        "uart_channel": resolve_kconfig_choice_macro(
            symbols,
            CVCC_UART_CHANNEL_SYMBOL_TO_MACRO,
            "Kconfig 中未选择 CVCC UART Channel，无法生成 CVCC 配置。",
        ),
        "ics": cvcc_cfg_ics,
        "k_array_rows": k_array_rows,
    }


def build_cvcc_cfg_placeholders(
    cvcc_cfg_domain: dict[str, Any],
    required_placeholders: set[str],
) -> dict[str, str]:
    cvcc_placeholder_required = any(
        name in {
            "CVCC_IC_TYPE",
            "CVCC_UART_CHANNEL",
            "USED_CVCC_CHANNEL_NUMS",
            "CVCC_K_ARRAY_ROWS",
        }
        or (name.startswith("CVCC_CFG_IC") and (
            name.endswith("_ADDR")
            or name.endswith("_USED_SWITCH")
            or name.endswith("_SWITCH_MASK")
            or name.endswith("_MAX_CURRENT")
        ))
        for name in required_placeholders
    )
    if not cvcc_placeholder_required:
        return {}

    placeholders: dict[str, str] = {}
    if "CVCC_IC_TYPE" in required_placeholders:
        placeholders["CVCC_IC_TYPE"] = str(cvcc_cfg_domain["ic_type"])
    if "CVCC_UART_CHANNEL" in required_placeholders:
        placeholders["CVCC_UART_CHANNEL"] = str(cvcc_cfg_domain["uart_channel"])
    if "USED_CVCC_CHANNEL_NUMS" in required_placeholders:
        placeholders["USED_CVCC_CHANNEL_NUMS"] = str(CVCC_K_ARRAY_FIXED_CHANNEL_COUNT)
    if "CVCC_K_ARRAY_ROWS" in required_placeholders:
        k_array_rows = cvcc_cfg_domain.get("k_array_rows")
        if not isinstance(k_array_rows, list):
            raise ValueError("cvcc_cfg 缺少 k_array_rows，无法生成占位符。")
        placeholders["CVCC_K_ARRAY_ROWS"] = format_cvcc_k_array_rows(k_array_rows)

    cvcc_cfg_ics = cvcc_cfg_domain.get("ics")
    if not isinstance(cvcc_cfg_ics, dict):
        raise ValueError("cvcc_cfg 缺少 ics，无法生成占位符。")

    for ic_index in CVCC_CFG_IC_ADDR_INDEXES:
        ic_name = f"IC{ic_index}"
        ic_payload = cvcc_cfg_ics.get(ic_name)
        if not isinstance(ic_payload, dict):
            raise ValueError(f"cvcc_cfg 缺少 {ic_name}，无法生成占位符。")

        placeholders[f"CVCC_CFG_IC{ic_index}_ADDR"] = format_cvcc_cfg_ic_addr_value(int(ic_payload["addr"]))
        placeholders[f"CVCC_CFG_IC{ic_index}_USED_SWITCH"] = format_cvcc_cfg_used_switch_value(int(ic_payload["used_switch"]))
        placeholders[f"CVCC_CFG_IC{ic_index}_SWITCH_MASK"] = str(ic_payload["switch_mask"])
        placeholders[f"CVCC_CFG_IC{ic_index}_MAX_CURRENT"] = format_cvcc_cfg_max_current_value(int(ic_payload["max_current"]))

    return placeholders


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


def parse_raw_signal_animation_sheet_name(sheet_name: str) -> tuple[str, int] | None:
    match = RAW_SIGNAL_ANIMATION_SHEET_PATTERN.fullmatch(sheet_name.strip())
    if match is None:
        return None
    return match.group(1).lower(), int(match.group(2))


def validate_raw_signal_animation_payload(
    sheet_name: str,
    payload: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], int]:
    columns = payload.get("columns")
    frames = payload.get("frames")
    column_count = payload.get("column_count")

    if not isinstance(columns, list) or not isinstance(frames, list):
        raise ValueError(f"{sheet_name}.json 缺少 columns/frames，无法生成动画配置。")
    if isinstance(column_count, bool) or not isinstance(column_count, int):
        raise ValueError(f"{sheet_name}.json 缺少有效的 column_count。")
    if len(columns) != column_count:
        raise ValueError(f"{sheet_name}.json 的 column_count 与 columns 长度不一致。")

    return columns, frames, column_count


def build_raw_signal_animation_domain(excel_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    domain = {
        kind_name: {
            "mode_count": 0,
            "mode_steps": [0] * ANIMATION_CFG_MAX_MODE_COUNT,
            "mode_payloads": {},
        }
        for kind_name in ANIMATION_CFG_KIND_NAMES
    }

    for sheet_name, payload in excel_payloads.items():
        parsed = parse_raw_signal_animation_sheet_name(sheet_name)
        if parsed is None:
            continue

        kind_name, mode_index = parsed
        if not 1 <= mode_index <= ANIMATION_CFG_MAX_MODE_COUNT:
            raise ValueError(
                f"{sheet_name}.json 的模式序号超出范围 1..{ANIMATION_CFG_MAX_MODE_COUNT}。"
            )

        validate_raw_signal_animation_payload(sheet_name, payload)
        kind_domain = domain[kind_name]
        mode_payloads = kind_domain["mode_payloads"]
        if mode_index in mode_payloads:
            raise ValueError(f"存在重复的 {kind_name} Mode{mode_index}.json。")

        frames = payload["frames"]
        mode_payloads[mode_index] = payload
        kind_domain["mode_steps"][mode_index - 1] = len(frames)

    for kind_name in ANIMATION_CFG_KIND_NAMES:
        kind_domain = domain[kind_name]
        kind_domain["mode_count"] = len(kind_domain["mode_payloads"])

    return domain


def build_raw_signal_animation_mode_body(payload: dict[str, Any]) -> str:
    sheet_name = str(payload.get("sheet_name", "raw_signal_animation"))
    columns, frames, column_count = validate_raw_signal_animation_payload(sheet_name, payload)
    if not frames:
        return "    /* UNUSED */"
    return (
        f"/**<  {format_e01_ads_animation_header(columns)} */\n"
        f"{format_e01_ads_animation_rows(frames, column_count)}"
    )


def build_raw_signal_animation_placeholders(
    animation_domain: dict[str, Any],
    required_placeholders: set[str],
) -> dict[str, Any]:
    animation_placeholder_required = any(
        name in {
            "LOCK_MODE_TYPE_NUMS",
            "UNLOCK_MODE_TYPE_NUMS",
            "LOCK_UNLOCK_ANIMATION_TOTAL_STEPS_ROWS",
            "LOCK_MODE1_ANIMATION_HEADER",
            "LOCK_MODE1_ANIMATION_ROWS",
            "UNLOCK_MODE1_ANIMATION_HEADER",
            "UNLOCK_MODE1_ANIMATION_ROWS",
        }
        or ((name.startswith("LOCK_MODE") or name.startswith("UNLOCK_MODE")) and name.endswith("_TOTAL_STEP"))
        or ((name.startswith("LOCK_MODE") or name.startswith("UNLOCK_MODE")) and name.endswith("_ANIMATION_BODY"))
        for name in required_placeholders
    )
    if not animation_placeholder_required:
        return {}

    placeholders: dict[str, Any] = {}
    animation_rows: list[tuple[str, int]] = []

    for kind_name in ANIMATION_CFG_KIND_NAMES:
        kind_domain = animation_domain.get(kind_name)
        if not isinstance(kind_domain, dict):
            raise ValueError(f"signal_animation 缺少 {kind_name} 配置。")

        mode_count = kind_domain.get("mode_count")
        mode_steps = kind_domain.get("mode_steps")
        mode_payloads = kind_domain.get("mode_payloads")
        if isinstance(mode_count, bool) or not isinstance(mode_count, int):
            raise ValueError(f"signal_animation.{kind_name}.mode_count 配置无效。")
        if not isinstance(mode_steps, list) or len(mode_steps) != ANIMATION_CFG_MAX_MODE_COUNT:
            raise ValueError(f"signal_animation.{kind_name}.mode_steps 配置无效。")
        if not isinstance(mode_payloads, dict):
            raise ValueError(f"signal_animation.{kind_name}.mode_payloads 配置无效。")

        if kind_name == "lock" and "LOCK_MODE_TYPE_NUMS" in required_placeholders:
            placeholders["LOCK_MODE_TYPE_NUMS"] = mode_count
        if kind_name == "unlock" and "UNLOCK_MODE_TYPE_NUMS" in required_placeholders:
            placeholders["UNLOCK_MODE_TYPE_NUMS"] = mode_count

        mode1_payload = mode_payloads.get(1)
        if mode1_payload is not None:
            sheet_name = str(mode1_payload.get("sheet_name", f"{kind_name} Mode1"))
            columns, frames, column_count = validate_raw_signal_animation_payload(sheet_name, mode1_payload)
            header = format_e01_ads_animation_header(columns)
            rows = format_e01_ads_animation_rows(frames, column_count)
        else:
            header = ""
            rows = ""

        header_placeholder = f"{kind_name.upper()}_MODE1_ANIMATION_HEADER"
        rows_placeholder = f"{kind_name.upper()}_MODE1_ANIMATION_ROWS"
        if header_placeholder in required_placeholders:
            placeholders[header_placeholder] = header
        if rows_placeholder in required_placeholders:
            placeholders[rows_placeholder] = rows

        for mode_index, total_steps in enumerate(mode_steps, start=1):
            placeholders[f"{kind_name.upper()}_MODE{mode_index}_TOTAL_STEP"] = int(total_steps)
            animation_rows.append((f"{kind_name.upper()}_MODE{mode_index}", int(total_steps)))

        for mode_index in range(2, ANIMATION_CFG_MAX_MODE_COUNT + 1):
            placeholder_name = f"{kind_name.upper()}_MODE{mode_index}_ANIMATION_BODY"
            if placeholder_name not in required_placeholders:
                continue

            payload = mode_payloads.get(mode_index)
            placeholders[placeholder_name] = "    /* UNUSED */" if payload is None else build_raw_signal_animation_mode_body(payload)

    if "LOCK_UNLOCK_ANIMATION_TOTAL_STEPS_ROWS" in required_placeholders:
        value_width = max(len(f"{total_steps}U") for _label, total_steps in animation_rows)
        lines: list[str] = []
        for index, (label, total_steps) in enumerate(animation_rows):
            suffix = "," if index < len(animation_rows) - 1 else ""
            lines.append(f"    {f'{total_steps}U':<{value_width}}{suffix}   /* {label:<12} */")
        placeholders["LOCK_UNLOCK_ANIMATION_TOTAL_STEPS_ROWS"] = "\n".join(lines)

    return placeholders


def normalize_e01_ads_animation_label(column_payload: dict[str, Any]) -> str:
    section_name = column_payload.get("section_name")
    if isinstance(section_name, str) and section_name.strip():
        return section_name.strip()

    output_name = column_payload.get("output_name")
    if isinstance(output_name, str) and output_name.strip():
        compact = output_name.replace("\r\n", "\n").replace("\n", ":")
        if ":" in compact:
            compact = compact.split(":")[-1]
        compact = compact.strip()
        if compact:
            return compact

    led_name = column_payload.get("led_name")
    if isinstance(led_name, str) and led_name.strip():
        return led_name.strip()
    return f"COL{int(column_payload.get('column_id', 0))}"


def format_e01_ads_animation_header(columns: list[dict[str, Any]]) -> str:
    grouped_labels: list[list[Any]] = []
    for column_payload in columns:
        label = normalize_e01_ads_animation_label(column_payload)
        if not grouped_labels or grouped_labels[-1][0] != label:
            grouped_labels.append([label, 1])
        else:
            grouped_labels[-1][1] += 1

    return "  ".join(
        label if count == 1 else f"{label} x{count}"
        for label, count in grouped_labels
    )


def format_signal_animation_rows(row_frames: list[tuple[list[int], int]]) -> str:
    value_width = 0
    time_width = 0

    lines: list[str] = []
    for values, time_ms in row_frames:
        for value in values:
            value_width = max(value_width, len(f"{value}U"))
        time_width = max(time_width, len(str(time_ms)))

    for values, time_ms in row_frames:
        formatted_values = [f"{value}U".ljust(value_width) for value in values]
        lines.append(
            f"    {{ {', '.join(formatted_values)} }}, /**< {time_ms:>{time_width}}ms */"
        )

    return "\n".join(lines)


def load_animation_board_type_map(path: Path) -> dict[str, Any]:
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} 必须是 JSON 对象。")

    source = payload.get("source")
    if not isinstance(source, str) or not source.strip():
        raise ValueError(f"{path} 缺少有效的 source。")

    board_type_map = payload.get("board_type_map")
    if not isinstance(board_type_map, dict):
        raise ValueError(f"{path} 缺少对象字段 board_type_map。")

    normalized_map: dict[str, int] = {}
    for board_name, type_value in board_type_map.items():
        if not isinstance(board_name, str) or not board_name.strip():
            raise ValueError(f"{path} 中存在无效灯板名 {board_name!r}。")
        if isinstance(type_value, bool) or not isinstance(type_value, int):
            raise ValueError(f"{path} 中 {board_name!r} 的 type 必须是整数。")
        normalized_map[board_name.strip()] = type_value

    return {
        "source": source.strip(),
        "board_type_map": normalized_map,
    }


def build_animation_board_types_domain(
    signal_animation: dict[str, Any],
    animation_board_type_map: dict[str, Any],
) -> dict[str, Any]:
    source = animation_board_type_map["source"]
    board_type_map = animation_board_type_map["board_type_map"]

    parsed = parse_raw_signal_animation_sheet_name(source)
    if parsed is None:
        raise ValueError(f"动画映射 source {source!r} 无法解析，请使用类似 'Unlock Mode1' 的 sheet 名。")
    kind_name, mode_index = parsed
    kind_domain = signal_animation.get(kind_name)
    if not isinstance(kind_domain, dict):
        raise ValueError(f"signal_animation 缺少 {kind_name} 配置。")
    mode_payloads = kind_domain.get("mode_payloads")
    if not isinstance(mode_payloads, dict):
        raise ValueError(f"signal_animation.{kind_name}.mode_payloads 配置无效。")
    source_payload = mode_payloads.get(mode_index)
    if not isinstance(source_payload, dict):
        raise ValueError(f"signal_animation 中缺少 {source} 动画数据。")

    columns, _frames, _column_count = validate_raw_signal_animation_payload(source, source_payload)

    by_board: dict[str, dict[str, Any]] = {}
    unmapped_boards: set[str] = set()
    for column_payload in columns:
        section_name = column_payload.get("section_name")
        if not isinstance(section_name, str) or not section_name.strip():
            raise ValueError(f"{source} 存在缺少 section_name 的动画列，无法建立灯板映射。")
        board_name = section_name.strip()
        if board_name not in board_type_map:
            unmapped_boards.add(board_name)
            continue

        board_entry = by_board.setdefault(
            board_name,
            {
                "type": int(board_type_map[board_name]),
                "column_ids": [],
                "column_count": 0,
                "start_column_id": None,
            },
        )
        column_id = column_payload.get("column_id")
        if isinstance(column_id, bool) or not isinstance(column_id, int):
            raise ValueError(f"{source} 的 {board_name} 存在无效 column_id。")
        board_entry["column_ids"].append(column_id)
        board_entry["column_count"] += 1
        current_start_column_id = board_entry["start_column_id"]
        if current_start_column_id is None or column_id < current_start_column_id:
            board_entry["start_column_id"] = column_id

    if unmapped_boards:
        missing = ", ".join(sorted(unmapped_boards))
        raise ValueError(f"{source} 中存在未映射的灯板，请补充 {ANIMATION_BOARD_TYPE_MAP_DEFAULT}: {missing}。")

    return {
        "source": source,
        "board_type_map": board_type_map,
        "by_board": by_board,
    }


def build_animation_offset_candidates_domain(
    signal_animation: dict[str, Any],
    animation_board_types: dict[str, Any],
) -> dict[str, Any]:
    source = animation_board_types["source"]
    parsed = parse_raw_signal_animation_sheet_name(source)
    if parsed is None:
        raise ValueError(f"动画映射 source {source!r} 无法解析。")
    kind_name, mode_index = parsed
    kind_domain = signal_animation.get(kind_name)
    if not isinstance(kind_domain, dict):
        raise ValueError(f"signal_animation 缺少 {kind_name} 配置。")
    mode_payloads = kind_domain.get("mode_payloads")
    if not isinstance(mode_payloads, dict):
        raise ValueError(f"signal_animation.{kind_name}.mode_payloads 配置无效。")
    source_payload = mode_payloads.get(mode_index)
    if not isinstance(source_payload, dict):
        raise ValueError(f"signal_animation 中缺少 {source} 动画数据。")

    columns, frames, _column_count = validate_raw_signal_animation_payload(source, source_payload)
    first_lit_by_column: dict[int, tuple[int, int]] = {}
    for frame_index, frame in enumerate(frames):
        values = frame.get("values")
        if not isinstance(values, list):
            raise ValueError(f"{source} 存在无效帧 values。")
        time_ms = frame.get("time_ms")
        if isinstance(time_ms, bool) or not isinstance(time_ms, int):
            raise ValueError(f"{source} 存在无效 time_ms。")
        for column_index, value in enumerate(values):
            if column_index in first_lit_by_column:
                continue
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"{source} 第 {frame_index} 帧存在非整数亮度值。")
            if value != 0:
                first_lit_by_column[column_index] = (frame_index, time_ms)

    columns_by_id = {
        int(column_payload["column_id"]): column_payload
        for column_payload in columns
        if isinstance(column_payload.get("column_id"), int) and not isinstance(column_payload.get("column_id"), bool)
    }

    by_type: dict[str, dict[str, Any]] = {}
    for board_name, board_payload in animation_board_types["by_board"].items():
        type_key = str(board_payload["type"])
        type_entry = by_type.setdefault(
            type_key,
            {
                "board_names": [],
                "matched_columns": [],
                "first_lit_frame": None,
                "first_lit_time_ms": None,
                "candidate_offset": 255,
            },
        )
        type_entry["board_names"].append(board_name)
        for column_id in board_payload["column_ids"]:
            column_payload = columns_by_id.get(column_id)
            if column_payload is None:
                raise ValueError(f"{source} 中缺少 column_id={column_id} 的列配置。")
            first_lit = first_lit_by_column.get(column_id)
            type_entry["matched_columns"].append(
                {
                    "column_id": column_id,
                    "output_name": column_payload.get("output_name", ""),
                    "section_name": column_payload.get("section_name", ""),
                    "first_lit_frame": None if first_lit is None else first_lit[0],
                    "first_lit_time_ms": None if first_lit is None else first_lit[1],
                }
            )
            if first_lit is None:
                continue
            first_frame, first_time_ms = first_lit
            current_first_frame = type_entry["first_lit_frame"]
            if current_first_frame is None or first_frame < current_first_frame:
                type_entry["first_lit_frame"] = first_frame
                type_entry["first_lit_time_ms"] = first_time_ms
                type_entry["candidate_offset"] = first_frame

        type_entry["board_names"].sort()
        type_entry["matched_columns"].sort(key=lambda item: int(item["column_id"]))

    return {
        "source": source,
        "by_type": by_type,
    }


def build_animation_start_column_placeholders(
    animation_board_types: dict[str, Any],
    required_placeholders: set[str],
) -> dict[str, int]:
    placeholders = {
        "CH_CFG_TYPE0_UNLOCK_LOCK_OFFSET": 255,
        "CH_CFG_TYPE2_UNLOCK_LOCK_OFFSET": 255,
        "CH_CFG_TYPE3_UNLOCK_LOCK_OFFSET": 255,
        "CH_CFG_TYPE4_UNLOCK_LOCK_OFFSET": 255,
        "CH_CFG_TYPE5_UNLOCK_LOCK_OFFSET": 255,
        "CH_CFG_TYPE6_UNLOCK_LOCK_OFFSET": 255,
        "CH_CFG_TYPE7_UNLOCK_LOCK_OFFSET": 255,
        "CH_CFG_TYPE8_UNLOCK_LOCK_OFFSET": 255,
        "PL_0_UNLOCK_LOCK_OFFSET": 255,
    }
    placeholder_by_type = {
        0: "CH_CFG_TYPE0_UNLOCK_LOCK_OFFSET",
        2: "CH_CFG_TYPE2_UNLOCK_LOCK_OFFSET",
        3: "CH_CFG_TYPE3_UNLOCK_LOCK_OFFSET",
        4: "CH_CFG_TYPE4_UNLOCK_LOCK_OFFSET",
        5: "CH_CFG_TYPE5_UNLOCK_LOCK_OFFSET",
        6: "CH_CFG_TYPE6_UNLOCK_LOCK_OFFSET",
        7: "CH_CFG_TYPE7_UNLOCK_LOCK_OFFSET",
        8: "CH_CFG_TYPE8_UNLOCK_LOCK_OFFSET",
    }

    for board_payload in animation_board_types.get("by_board", {}).values():
        type_id = board_payload.get("type")
        start_column_id = board_payload.get("start_column_id")
        if isinstance(type_id, bool) or not isinstance(type_id, int):
            raise ValueError("animation_board_types 中存在无效 type。")
        if isinstance(start_column_id, bool) or not isinstance(start_column_id, int):
            continue
        placeholder_name = placeholder_by_type.get(type_id)
        if placeholder_name is None:
            continue
        current_value = placeholders[placeholder_name]
        if start_column_id < current_value:
            placeholders[placeholder_name] = start_column_id

    return {
        name: value
        for name, value in placeholders.items()
        if name in required_placeholders
    }


def format_e01_ads_animation_rows(frames: list[dict[str, Any]], column_count: int) -> str:
    normalized_frames: list[tuple[list[int], int]] = []

    for frame in frames:
        values = frame.get("values")
        if not isinstance(values, list) or len(values) != column_count:
            raise ValueError("E01 ADS 原始动画帧列数无效，无法生成 C 数组。")

        normalized_values: list[int] = []
        for value in values:
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError("E01 ADS 原始动画存在非整数像素值，无法生成 C 数组。")
            normalized_values.append(value)

        time_ms = frame.get("time_ms")
        if isinstance(time_ms, bool) or not isinstance(time_ms, int):
            raise ValueError("E01 ADS 原始动画存在无效 time_ms，无法生成 C 数组。")

        normalized_frames.append((normalized_values, time_ms))

    return format_signal_animation_rows(normalized_frames)


def parse_ti_sequential_channel_name(channel_name: str, channel_count_per_ic: int) -> tuple[int, int]:
    match = TI_SEQUENTIAL_CHANNEL_PATTERN.fullmatch(channel_name)
    if match is None:
        raise ValueError(f"TI_sequential 存在无效通道名 {channel_name!r}。")

    ic_index = int(match.group(1))
    channel_index = int(match.group(2))
    if channel_index >= channel_count_per_ic:
        raise ValueError(
            f"TI_sequential 通道 {channel_name!r} 超出每颗 IC 的通道范围 0..{channel_count_per_ic - 1}。"
        )
    return ic_index, channel_index


def validate_ti_sequential_payload(payload: dict[str, Any]) -> tuple[list[tuple[int, dict[str, int]]], list[str]]:
    animation = require_dict(payload, "animation", "TI_sequential")
    frames = animation.get("frames")
    if not isinstance(frames, list) or not frames:
        raise ValueError("TI_sequential 缺少有效的 animation.frames，无法生成 TI 流水表。")

    channel_count_per_ic = payload.get("channel_count_per_ic")
    if isinstance(channel_count_per_ic, bool) or not isinstance(channel_count_per_ic, int) or channel_count_per_ic <= 0:
        raise ValueError("TI_sequential 缺少有效的 channel_count_per_ic，无法生成 TI 流水表。")

    normalized_frames: list[tuple[int, dict[str, int]]] = []
    ordered_channel_map: dict[str, tuple[int, int]] = {}

    for frame in frames:
        if not isinstance(frame, dict):
            raise ValueError("TI_sequential 存在无效帧，无法生成 TI 流水表。")

        time_ms = frame.get("time_ms")
        if isinstance(time_ms, bool) or not isinstance(time_ms, int):
            raise ValueError("TI_sequential 存在无效 time_ms，无法生成 TI 流水表。")

        channels = frame.get("channels")
        if not isinstance(channels, dict):
            raise ValueError("TI_sequential 存在无效 channels，无法生成 TI 流水表。")

        normalized_channels: dict[str, int] = {}
        for channel_name, value in channels.items():
            if not isinstance(channel_name, str):
                raise ValueError("TI_sequential 存在非字符串通道名，无法生成 TI 流水表。")
            if isinstance(value, bool) or not isinstance(value, int):
                raise ValueError(f"TI_sequential 通道 {channel_name!r} 的 PWM 值必须是整数。")

            channel_key = parse_ti_sequential_channel_name(channel_name, channel_count_per_ic)
            ordered_channel_map[channel_name] = channel_key
            normalized_channels[channel_name] = value

        normalized_frames.append((time_ms, normalized_channels))

    ordered_channels = [
        channel_name
        for channel_name, _channel_key in sorted(
            ordered_channel_map.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    ]
    if not ordered_channels:
        raise ValueError("TI_sequential 未找到任何有效通道，无法生成 TI 流水表。")

    return normalized_frames, ordered_channels


def format_ti_sequential_header(ordered_channels: list[str], channel_count_per_ic: int) -> str:
    labels: list[str] = []
    for channel_name in ordered_channels:
        ic_index, channel_index = parse_ti_sequential_channel_name(channel_name, channel_count_per_ic)
        led_index = ((ic_index - 2) * 8 + channel_index) // 2 + 1
        labels.append(f"TI{led_index:02d}")
    return "  ".join(labels)


def build_ti_sequential_placeholders(
    excel_payloads: dict[str, dict[str, Any]],
    required_placeholders: set[str],
) -> dict[str, str]:
    ti_placeholder_required = any(
        name in {"TI_SWEEP_LED_K_HEADER", "TI_SWEEP_LED_K_ROWS"}
        for name in required_placeholders
    )
    if not ti_placeholder_required:
        return {}

    payload = require_excel_payload(excel_payloads, "TI_sequential", purpose="生成 TI 流水动画占位符")
    normalized_frames, ordered_channels = validate_ti_sequential_payload(payload)
    channel_count_per_ic = int(payload["channel_count_per_ic"])

    row_frames = [
        ([channels.get(channel_name, 0) for channel_name in ordered_channels], time_ms)
        for time_ms, channels in normalized_frames
    ]

    placeholders: dict[str, str] = {}
    if "TI_SWEEP_LED_K_HEADER" in required_placeholders:
        placeholders["TI_SWEEP_LED_K_HEADER"] = format_ti_sequential_header(ordered_channels, channel_count_per_ic)
    if "TI_SWEEP_LED_K_ROWS" in required_placeholders:
        placeholders["TI_SWEEP_LED_K_ROWS"] = format_signal_animation_rows(row_frames)
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
    animation_board_type_map: dict[str, Any],
) -> dict[str, Any]:
    ch_cfg_channel_types, current_effective_channels = validate_channel_config_consistency(excel_payloads)
    placeholders = {**SCALAR_DEFAULTS, **extract_scalar_placeholders(kconfig_payload, excel_payloads)}
    sections: dict[str, str] = {}
    cvcc_cfg = build_cvcc_cfg_domain(excel_payloads, kconfig_payload)
    ch_cfg_channel_counts = build_ch_cfg_channel_counts_domain(excel_payloads)
    ch_cfg_fixed_currents = build_ch_cfg_fixed_currents_domain(excel_payloads, ch_cfg_channel_types, current_effective_channels)
    signal_animation = build_raw_signal_animation_domain(excel_payloads)
    animation_board_types = build_animation_board_types_domain(signal_animation, animation_board_type_map)
    animation_offset_candidates = build_animation_offset_candidates_domain(signal_animation, animation_board_types)
    placeholders.update(build_cvcc_cfg_placeholders(cvcc_cfg, required_placeholders))
    placeholders.update(build_raw_signal_animation_placeholders(signal_animation, required_placeholders))
    placeholders.update(build_animation_start_column_placeholders(animation_board_types, required_placeholders))
    placeholders.update(build_ti_sequential_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_type0_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_type1_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_type2_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_type3_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_type4_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_type5_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_type6_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_type7_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_type8_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_type9_placeholders(excel_payloads, required_placeholders))
    placeholders.update(build_ch_cfg_fixed_current_placeholders(ch_cfg_fixed_currents, required_placeholders))
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
        "cvcc_cfg": cvcc_cfg,
        "ch_cfg_channel_counts": ch_cfg_channel_counts,
        "ch_cfg_fixed_currents": ch_cfg_fixed_currents,
        "signal_animation": signal_animation,
        "animation_board_types": animation_board_types,
        "animation_offset_candidates": animation_offset_candidates,
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
    parser.add_argument(
        "--animation-board-type-map",
        type=Path,
        default=ANIMATION_BOARD_TYPE_MAP_DEFAULT,
        help=f"Animation board/type map JSON path. Default: {ANIMATION_BOARD_TYPE_MAP_DEFAULT}",
    )
    return parser


def format_error_message(message: str) -> str:
    if not sys.stderr.isatty():
        return f"Error: {message}"
    return f"{ANSI_BOLD}{ANSI_RED}Error:{ANSI_RESET} {ANSI_RED}{message}{ANSI_RESET}"


def main() -> None:
    args = build_parser().parse_args()
    try:
        excluded_files = {args.kconfig_json.resolve(), args.output.resolve()}
        excel_payloads = load_excel_jsons(args.input_dir, excluded_files)
        kconfig_payload = load_json(args.kconfig_json)
        animation_board_type_map = load_animation_board_type_map(args.animation_board_type_map)
        required_placeholders = load_required_placeholders(args.header_template, args.source_template)

        payload = build_render_context(
            excel_payloads,
            kconfig_payload,
            required_placeholders,
            animation_board_type_map,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(render_json_compact(payload) + "\n", encoding="utf-8")
    except Exception as exc:
        print(format_error_message(str(exc)), file=sys.stderr)
        raise SystemExit(1) from None

    print(f"Input dir: {args.input_dir}")
    print(f"Kconfig JSON: {args.kconfig_json}")
    print(f"Animation board/type map: {args.animation_board_type_map}")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

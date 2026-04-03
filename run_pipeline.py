from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
CONFIG_DEFAULT = Path(".config")
KCONFIG_DEFAULT = Path("Kconfig")
OUTPUT_DIR_DEFAULT = Path("output")
HEADER_TEMPLATE_DEFAULT = Path("templates") / "app_config.h.tpl"
SOURCE_TEMPLATE_DEFAULT = Path("templates") / "app_config.c.tpl"
ANIMATION_BOARD_TYPE_MAP_DEFAULT = Path("animation_board_type_map.json")
ANSI_RED = "\033[31m"
ANSI_BOLD = "\033[1m"
ANSI_RESET = "\033[0m"


def format_error_message(message: str) -> str:
    if not sys.stderr.isatty():
        return message
    return f"{ANSI_BOLD}{ANSI_RED}{message}{ANSI_RESET}"


def run_step(step_no: int, total_steps: int, title: str, command: list[str]) -> None:
    print(f"[{step_no}/{total_steps}] {title}", flush=True)
    print(" ".join(command), flush=True)
    try:
        subprocess.run(command, cwd=REPO_ROOT, check=True)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(format_error_message(f"Step failed [{step_no}/{total_steps}] {title}")) from None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the full CHCM config conversion pipeline.")
    parser.add_argument(
        "--workbook",
        type=Path,
        default=None,
        help="Workbook path. Overrides the value loaded from .config and Kconfig.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=CONFIG_DEFAULT,
        help=f"Kconfig .config path. Default: {CONFIG_DEFAULT}",
    )
    parser.add_argument(
        "--kconfig",
        type=Path,
        default=KCONFIG_DEFAULT,
        help=f"Kconfig file path. Default: {KCONFIG_DEFAULT}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR_DEFAULT,
        help=f"Output directory for generated JSON and app_config files. Default: {OUTPUT_DIR_DEFAULT}",
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
        "--animation-board-type-map",
        type=Path,
        default=ANIMATION_BOARD_TYPE_MAP_DEFAULT,
        help=f"Animation board/type map JSON path. Default: {ANIMATION_BOARD_TYPE_MAP_DEFAULT}",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_dir = args.output_dir
    kconfig_json = output_dir / "Kconfig.json"
    render_context = output_dir / "render_context.json"
    header_output = output_dir / "app_config.h"
    source_output = output_dir / "app_config.c"

    extract_command = [
        sys.executable,
        "extract_excel_json.py",
        "--config",
        str(args.config),
        "--output",
        str(output_dir),
    ]
    if args.workbook is not None:
        extract_command.extend(["--workbook", str(args.workbook)])

    kconfig_command = [
        sys.executable,
        "kconfig_to_json.py",
        "--kconfig",
        str(args.kconfig),
        "--config",
        str(args.config),
        "--output",
        str(kconfig_json),
    ]

    build_context_command = [
        sys.executable,
        "build_render_context.py",
        "--input-dir",
        str(output_dir),
        "--kconfig-json",
        str(kconfig_json),
        "--header-template",
        str(args.header_template),
        "--source-template",
        str(args.source_template),
        "--animation-board-type-map",
        str(args.animation_board_type_map),
        "--output",
        str(render_context),
    ]

    render_command = [
        sys.executable,
        "render_app_config.py",
        "--context",
        str(render_context),
        "--header-template",
        str(args.header_template),
        "--source-template",
        str(args.source_template),
        "--header-output",
        str(header_output),
        "--source-output",
        str(source_output),
    ]

    total_steps = 4
    run_step(1, total_steps, "Extract Excel JSON", extract_command)
    run_step(2, total_steps, "Export Kconfig JSON", kconfig_command)
    run_step(3, total_steps, "Build render_context.json", build_context_command)
    run_step(4, total_steps, "Render app_config.c and app_config.h", render_command)

    print("Pipeline completed.")
    print(f"Wrote {header_output}")
    print(f"Wrote {source_output}")


if __name__ == "__main__":
    main()

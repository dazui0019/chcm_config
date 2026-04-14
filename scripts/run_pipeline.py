from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

from extract_excel_json import is_supported_sheet_name, resolve_workbook_path
from pipeline_utils import load_pipeline_state, save_pipeline_state

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
RESOURCE_DIR = PROJECT_ROOT / "resources"
TEMPLATE_DIR = RESOURCE_DIR / "templates"
CONFIG_DEFAULT = PROJECT_ROOT / ".config"
KCONFIG_DEFAULT = PROJECT_ROOT / "Kconfig"
OUTPUT_DIR_DEFAULT = PROJECT_ROOT / "output"
HEADER_TEMPLATE_DEFAULT = TEMPLATE_DIR / "app_config.h.tpl"
SOURCE_TEMPLATE_DEFAULT = TEMPLATE_DIR / "app_config.c.tpl"
ANIMATION_BOARD_TYPE_MAP_DEFAULT = RESOURCE_DIR / "animation_board_type_map.json"
PIPELINE_STATE_DEFAULT = OUTPUT_DIR_DEFAULT / ".pipeline_state.json"
PIPELINE_RESERVED_JSON_NAMES = {"Kconfig.json", "render_context.json"}
ANSI_RED = "\033[31m"
ANSI_BOLD = "\033[1m"
ANSI_RESET = "\033[0m"


def format_error_message(message: str) -> str:
    if not sys.stderr.isatty():
        return message
    return f"{ANSI_BOLD}{ANSI_RED}{message}{ANSI_RESET}"


def resolve_paths(paths: list[Path]) -> list[Path]:
    return [path.resolve() for path in paths]


def snapshot_inputs(paths: list[Path]) -> list[dict[str, Any]]:
    snapshots: list[dict[str, Any]] = []
    for path in resolve_paths(paths):
        snapshots.append({
            "path": str(path),
            "mtime_ns": path.stat().st_mtime_ns,
        })
    return snapshots


def snapshot_outputs(paths: list[Path]) -> list[str]:
    return [str(path) for path in resolve_paths(paths)]


def parse_stored_input_mtimes(step_state: dict[str, Any]) -> dict[str, int] | None:
    stored_inputs = step_state.get("inputs")
    if not isinstance(stored_inputs, list):
        return None

    input_mtimes: dict[str, int] = {}
    for item in stored_inputs:
        if not isinstance(item, dict):
            return None
        path = item.get("path")
        mtime_ns = item.get("mtime_ns")
        if not isinstance(path, str) or not isinstance(mtime_ns, int):
            return None
        input_mtimes[path] = mtime_ns
    return input_mtimes


def parse_stored_outputs(step_state: dict[str, Any]) -> list[Path] | None:
    stored_outputs = step_state.get("outputs")
    if not isinstance(stored_outputs, list) or not stored_outputs:
        return None

    output_paths: list[Path] = []
    for item in stored_outputs:
        if not isinstance(item, str):
            return None
        output_paths.append(Path(item).resolve())
    return output_paths


def is_step_stale(
    state: dict[str, Any],
    step_name: str,
    input_paths: list[Path],
    output_paths: list[Path] | None = None,
) -> bool:
    step_state = state.get(step_name)
    if not isinstance(step_state, dict):
        return True

    resolved_inputs = resolve_paths(input_paths)
    stored_input_mtimes = parse_stored_input_mtimes(step_state)
    if stored_input_mtimes is None or len(stored_input_mtimes) != len(resolved_inputs):
        return True

    for path in resolved_inputs:
        if not path.is_file():
            return True
        if stored_input_mtimes.get(str(path)) != path.stat().st_mtime_ns:
            return True

    stored_output_paths = parse_stored_outputs(step_state)
    if stored_output_paths is None:
        return True

    if output_paths is not None:
        resolved_outputs = resolve_paths(output_paths)
        if sorted(str(path) for path in resolved_outputs) != sorted(str(path) for path in stored_output_paths):
            return True
    else:
        resolved_outputs = stored_output_paths

    return any(not path.is_file() for path in resolved_outputs)


def run_step(step_no: int, total_steps: int, title: str, command: list[str], should_run: bool) -> bool:
    action = "Run " if should_run else "Skip"
    print(f"[{step_no}/{total_steps}] {action} {title}", flush=True)
    if not should_run:
        return False

    print(" ".join(command), flush=True)
    try:
        subprocess.run(command, cwd=PROJECT_ROOT, check=True)
    except subprocess.CalledProcessError as exc:
        raise SystemExit(format_error_message(f"Step failed [{step_no}/{total_steps}] {title}")) from None
    return True


def is_excel_output_json_path(path: Path) -> bool:
    return (
        path.suffix.lower() == ".json"
        and path.name not in PIPELINE_RESERVED_JSON_NAMES
        and is_supported_sheet_name(path.stem)
    )


def list_excel_json_outputs(output_dir: Path) -> list[Path]:
    if not output_dir.is_dir():
        return []
    return sorted(
        (path.resolve() for path in output_dir.glob("*.json") if is_excel_output_json_path(path)),
        key=str,
    )


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
    output_dir = args.output_dir.resolve()
    kconfig_json = (output_dir / "Kconfig.json").resolve()
    render_context = (output_dir / "render_context.json").resolve()
    header_output = (output_dir / "app_config.h").resolve()
    source_output = (output_dir / "app_config.c").resolve()
    pipeline_state_path = (output_dir / PIPELINE_STATE_DEFAULT.name).resolve()
    state = load_pipeline_state(pipeline_state_path)
    workbook_path = resolve_workbook_path(args.workbook, args.config).resolve()

    extract_command = [
        sys.executable,
        str(SCRIPT_DIR / "extract_excel_json.py"),
        "--config",
        str(args.config),
        "--output",
        str(output_dir),
    ]
    if args.workbook is not None:
        extract_command.extend(["--workbook", str(args.workbook)])

    kconfig_command = [
        sys.executable,
        str(SCRIPT_DIR / "kconfig_to_json.py"),
        "--kconfig",
        str(args.kconfig),
        "--config",
        str(args.config),
        "--output",
        str(kconfig_json),
    ]

    build_context_command = [
        sys.executable,
        str(SCRIPT_DIR / "build_render_context.py"),
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
        str(SCRIPT_DIR / "render_app_config.py"),
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
    extract_inputs = [workbook_path, (SCRIPT_DIR / "extract_excel_json.py").resolve()]
    if args.workbook is None:
        extract_inputs.extend([args.config.resolve(), KCONFIG_DEFAULT.resolve()])
    extract_ran = run_step(
        1,
        total_steps,
        "Extract Excel JSON",
        extract_command,
        is_step_stale(state, "extract_excel_json", extract_inputs),
    )
    if extract_ran:
        state["extract_excel_json"] = {
            "inputs": snapshot_inputs(extract_inputs),
            "outputs": snapshot_outputs(list_excel_json_outputs(output_dir)),
        }
        save_pipeline_state(pipeline_state_path, state)

    excel_json_outputs = list_excel_json_outputs(output_dir)

    kconfig_inputs = [args.config.resolve(), args.kconfig.resolve(), (SCRIPT_DIR / "kconfig_to_json.py").resolve()]
    kconfig_outputs = [kconfig_json]
    kconfig_ran = run_step(
        2,
        total_steps,
        "Export Kconfig JSON",
        kconfig_command,
        is_step_stale(state, "kconfig_to_json", kconfig_inputs, kconfig_outputs),
    )
    if kconfig_ran:
        state["kconfig_to_json"] = {
            "inputs": snapshot_inputs(kconfig_inputs),
            "outputs": snapshot_outputs(kconfig_outputs),
        }
        save_pipeline_state(pipeline_state_path, state)

    build_context_inputs = [
        *excel_json_outputs,
        kconfig_json,
        args.header_template.resolve(),
        args.source_template.resolve(),
        args.animation_board_type_map.resolve(),
        (SCRIPT_DIR / "build_render_context.py").resolve(),
    ]
    build_context_outputs = [render_context]
    build_context_ran = run_step(
        3,
        total_steps,
        "Build render_context.json",
        build_context_command,
        extract_ran
        or kconfig_ran
        or is_step_stale(state, "build_render_context", build_context_inputs, build_context_outputs),
    )
    if build_context_ran:
        state["build_render_context"] = {
            "inputs": snapshot_inputs(build_context_inputs),
            "outputs": snapshot_outputs(build_context_outputs),
        }
        save_pipeline_state(pipeline_state_path, state)

    render_inputs = [
        render_context,
        args.header_template.resolve(),
        args.source_template.resolve(),
        (SCRIPT_DIR / "render_app_config.py").resolve(),
    ]
    render_outputs = [header_output, source_output]
    render_ran = run_step(
        4,
        total_steps,
        "Render app_config.c and app_config.h",
        render_command,
        build_context_ran or is_step_stale(state, "render_app_config", render_inputs, render_outputs),
    )
    if render_ran:
        state["render_app_config"] = {
            "inputs": snapshot_inputs(render_inputs),
            "outputs": snapshot_outputs(render_outputs),
        }
        save_pipeline_state(pipeline_state_path, state)

    print("Pipeline completed.")
    print(f"Header output: {header_output}")
    print(f"Source output: {source_output}")


if __name__ == "__main__":
    main()

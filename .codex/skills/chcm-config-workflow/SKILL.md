---
name: chcm-config-workflow
description: Maintain the CHCM config generation workflow in this repository. Use when working on scripts or templates that extract Excel config and Kconfig supplements into JSON, build output/render_context.json, or render output/app_config.c and output/app_config.h. Trigger for edits in extract_excel_json.py, kconfig_to_json.py, build_render_context.py, render_app_config.py, templates/app_config.c.tpl, templates/app_config.h.tpl, Kconfig, or the generated output files.
---

# CHCM Config Workflow

## Goal

Generate `output/app_config.c` and `output/app_config.h` from Excel data plus Kconfig supplements.

Treat Excel as the primary source for Excel-backed configuration items. Treat Kconfig as a supplement for extra configuration that is not maintained in Excel.

## Workflow

1. Run `uv run python extract_excel_json.py` to export supported Excel sheets into `output/*.json`.
2. Run `uv run python kconfig_to_json.py` to export Kconfig placeholders into `output/Kconfig.json`.
3. Run `uv run python build_render_context.py` to merge Excel JSON and Kconfig JSON into `output/render_context.json`.
4. Run `uv run python render_app_config.py --context output/render_context.json` to render `output/app_config.h` and `output/app_config.c`.

## Project Rules

- Keep `templates/app_config.h.tpl` and `templates/app_config.c.tpl` close to the reference `app_config` files.
- Replace content gradually, block by block. Avoid broad rewrites unless the user explicitly asks for them.
- Preserve existing macro names, typedefs, declarations, comments, and layout unless the user explicitly asks to rename or restructure them.
- For `.h` macro blocks, keep each `#define` line in the template and replace only the value part.
- For logically related `.c` and `.h` changes, treat them as one config domain and implement them through one shared entry point in `build_render_context.py`.
- Do not use Kconfig to override Excel-backed items unless the user explicitly changes that rule.
- Keep `render_app_config.py` as a pure renderer that only consumes `render_context.json`.
- Assemble generated snippets and placeholder values in `build_render_context.py`.
- Write generated files to `output/app_config.h` and `output/app_config.c` by default.

## Current Pipeline Files

- `extract_excel_json.py`: Excel workbook to per-sheet JSON.
- `kconfig_to_json.py`: `Kconfig` and `.config` to `output/Kconfig.json`.
- `build_render_context.py`: merged placeholder and section builder for `output/render_context.json`.
- `render_app_config.py`: template renderer for the final `.h` and `.c`.
- `templates/app_config.h.tpl` and `templates/app_config.c.tpl`: incremental templates based on the reference files.

## Current Implemented Blocks

- `PROJECT_NAME` replacement in `templates/app_config.h.tpl`.
- `SYSTEM_COM_VERION` replacement in `templates/app_config.c.tpl`.
- `CHCM_Cfg[]` value and comment replacement in `templates/app_config.c.tpl` from `output/HCM_PriLIN_Matrix.json`.
- `CHCM_CFG_IDX_*` and `CHCM_CFG_IDX_MAX` replacement in `templates/app_config.h.tpl`.
- `CHCM_Cfg[]` currently uses section `.parameter_config_61`.

## Unified Entry Rule

- When one logical feature affects both `templates/app_config.h.tpl` and `templates/app_config.c.tpl`, add one shared builder entry in `build_render_context.py` first, then fan out to the `.h` and `.c` placeholders from that shared result.
- Do not implement separate `.h` and `.c` data-loading paths for the same logical config block.
- Prefer one source-loading function, one domain-level placeholder builder, and then small output-specific placeholder builders.
- Use CHCM as the current reference pattern: shared source loading plus one unified CHCM placeholder entry, then separate `.h` index placeholders and `.c` item placeholders.

## CHCM Index Rules

- Keep each `CHCM_CFG_IDX_*` macro line explicitly in `templates/app_config.h.tpl`.
- Replace only the numeric part with placeholders such as `@CHCM_CFG_IDX_17_DC_MOTOR_LEVEL@`.
- Resolve each macro by mapping macro name to the Excel CFG name, then read the matching `id` from `HCM_PriLIN_Matrix.json`.
- Do not derive CHCM indexes from row order alone.
- Keep reserved indexes `20..26` fixed unless the user explicitly changes that contract.
- If a required CFG name is missing from Excel-derived JSON, fail loudly instead of guessing.

## Current Known Behavior

- `build_render_context.py` is the place to add new generated C blocks or value placeholders.
- `CHCM` is currently the reference implementation for a shared `.c`/`.h` logic block handled through one unified entry in `build_render_context.py`.
- `CHCM_Cfg[]` is currently kept expanded in `templates/app_config.c.tpl`, with item-level placeholders like `CHCM_CFG_ITEM_<id>_WORD0` and `CHCM_CFG_ITEM_<id>_COMMENT`.
- Multi-entry CHCM items `17` and `19` currently render as `{0U, 0U, 0U}` placeholders in `CHCM_Cfg[]` until the user asks for a richer encoding rule.
- `render_app_config.py` should not parse Excel directly.

## Editing Checklist

1. Change only the next requested block or placeholder set.
2. Keep the template structure recognizable to the user.
3. If the change logically spans both `.h` and `.c`, first create or extend one shared entry point in `build_render_context.py` for that domain.
4. Rebuild with:
   `uv run python build_render_context.py`
   `uv run python render_app_config.py --context output/render_context.json`
5. Verify the generated files under `output/`.
6. When asked to sync, commit only the intended changes and push to `origin/main` without touching unrelated user edits.

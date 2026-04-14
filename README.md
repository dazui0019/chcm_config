# chcm_config

1. `build_render_context.py`、`extract_excel_json.py`、`kconfig_to_json.py`和`render_app_config.py`用来从`excel`生成`c`文件。`run_pipeline.py`用来一次跑完所有以上用来生成`c`文件的`python`脚本。
2. `Sconstruct`用来将`c`源文件编译成单独的`app_config.elf`, `elf_tool.py`可以用来检查生成的`elf`中的符号地址是否正确。

## 仓库能做什么

- 从 Excel 工作簿中提取已支持的配置 sheet，并转换成结构化 JSON
- 从 `Kconfig/.config` 中提取配置项，生成 `Kconfig.json`
- 合并 Excel 与 Kconfig 数据，生成统一的 `render_context.json`
- 基于模板渲染 `app_config.h` 和 `app_config.c`
- 配合 `SCons` 继续完成目标产物的编译和链接

## 主要组成

- `scripts/`
  - 配置处理流水线的脚本入口
- `resources/templates/`
  - `app_config.h.tpl`、`app_config.c.tpl` 和模板说明
- `resources/animation_board_type_map.json`
  - 动画灯板映射配置
- `docs/`
  - 使用说明和专题文档
- `build/`
  - `SCons` 构建输出

## 典型流程

```text
Excel + Kconfig/.config
        ↓
extract_excel_json.py + kconfig_to_json.py
        ↓
build_render_context.py
        ↓
render_app_config.py
        ↓
app_config.h / app_config.c
        ↓
SCons build
```

如果只想直接跑完整链路，可以使用：

```powershell
uv sync
uv run python scripts/run_pipeline.py
```

## 当前支持的配置范围

- `HCM_PriLIN_Matrix`
- `CH_Cfg`
- `Lock ModeN` / `Unlock ModeN`
- `current_config`
- `Motor_Cfg`
- `TI_sequential`

## 文档入口

- 详细流水线说明：[`docs/chcm_config_pipeline.md`](docs/chcm_config_pipeline.md)
- 模板设计说明：[`resources/templates/README.md`](resources/templates/README.md)
- 其他文档：[`docs/elf_tool.md`](docs/elf_tool.md)、[`docs/sons.md`](docs/sons.md)

## 使用说明

如果你要了解整个配置生成流程、命令行参数、输出 JSON 结构和注意事项，直接看 [`docs/chcm_config_pipeline.md`](docs/chcm_config_pipeline.md)。

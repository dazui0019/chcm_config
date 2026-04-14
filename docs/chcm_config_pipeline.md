# CHCM Config Pipeline

`chcm_config` 用于把 CHCM 配置数据拆成清晰、可复用的生成链路：

1. 从 Excel 提取各个 sheet 的 JSON
2. 从 `Kconfig/.config` 提取配置 JSON
3. 合并为统一的 `render_context.json`
4. 渲染生成 `app_config.h` 和 `app_config.c`
5. 按需继续执行 `SCons` 构建

目前仓库已经把“数据提取”“业务合并”“模板渲染”“编译构建”分开，便于单独调试每一步。

## 处理流程

### 准备excel文件

把`(English+Chinese)E01_A+_ADS_CheryDatasetParameterList(to得邦).xlsx`中`E01 TI Wipping`、`Unlock Mode1`和`Lock Mode1`这三个sheet复制到`E01 CHCM-1C-2C1V(得邦)_config_Dataset_LEFT_V0.2.xlsx`, 用来获取动画数据。

### 分步脚本

- `scripts/extract_excel_json.py`
  - 读取 Excel 工作簿，提取已支持的 sheet，输出 JSON
- `scripts/kconfig_to_json.py`
  - 读取 `Kconfig/.config`，输出 `Kconfig.json`
- `scripts/build_render_context.py`
  - 合并 Excel JSON 和 Kconfig JSON，生成 `render_context.json`
- `scripts/render_app_config.py`
  - 读取 `render_context.json`，渲染 `app_config.h/.c`
- `scripts/run_pipeline.py`
  - 按顺序执行完整流程

### 一键流程

```powershell
uv run python scripts/run_pipeline.py
```

默认会顺序生成：

- `output/*.json`
- `output/Kconfig.json`
- `output/render_context.json`
- `output/app_config.h`
- `output/app_config.c`

## 目录结构

- `scripts/`
  - Python 脚本入口
- `resources/templates/`
  - `app_config.h.tpl`、`app_config.c.tpl` 及模板说明
- `resources/animation_board_type_map.json`
  - 动画灯板到 board type 的映射表
- `resources/linker/`
  - `SCons` 使用的 linker script
- `docs/`
  - 其他独立文档
- `build/`
  - `SCons` 构建输出
- `output/`
  - 配置生成链输出

## 当前支持的 Excel sheet

- `HCM_PriLIN_Matrix`
  - 矩阵类配置项，输出为统一的 `entries` 结构
- `CH_Cfg`
  - 通道类型配置，按 `ICx -> CHyy` 分组
- `Lock ModeN` / `Unlock ModeN`
  - 原始解闭锁动画 sheet，输出逐帧动画数据
- `current_config`
  - 通道电流、功能、系数配置
- `Motor_Cfg`
  - 步进电机和 AFS 相关配置
- `TI_sequential`
  - 单个 PWM 动画的逐帧通道值

脚本默认会在工作簿中查找所有当前已支持的 sheet 并批量转换。

## 环境准备

仓库使用 `uv` 管理 Python 依赖，要求 Python 版本为 `>=3.13`。

```powershell
uv sync
```

## Excel 路径配置

仓库通过 `Kconfig` 和 `.config` 管理 Excel 工作簿路径。

优先级从高到低如下：

1. 命令行 `--workbook`
2. `.config` 中的 `CONFIG_CHCM_WORKBOOK_PATH`
3. `Kconfig` 中的默认值

推荐先复制示例配置：

```powershell
Copy-Item .config.example .config
```

然后编辑 `.config`：

```text
CONFIG_CHCM_WORKBOOK_PATH="xlsx/E01 CHCM-1C-2C1V(得邦)_config_Dataset_LEFT_V0.2.xlsx"
```

`.config`、`xlsx/`、`output/` 都已加入 `.gitignore`，不会自动提交。

## 快速开始

### 1. 安装依赖

```powershell
uv sync
```

### 2. 准备 `.config`

```powershell
Copy-Item .config.example .config
```

按实际情况修改 `CONFIG_CHCM_WORKBOOK_PATH`。

### 3. 运行完整生成流程

```powershell
uv run python scripts/run_pipeline.py
```

### 4. 执行 SCons 构建

`Sconstruct` 会把 `../App/app_config.c` 和 `../App/app_swi/config/app_swi_config.c` 编译成 `.o`，再链接生成 `elf/bin/hex`：

```powershell
scons
```

## 脚本说明

### `scripts/run_pipeline.py`

适合日常使用，直接跑完整链路。

```powershell
uv run python scripts/run_pipeline.py --workbook <excel路径> --config <.config路径> --kconfig <Kconfig路径> --output-dir <输出目录>
```

常用参数：

- `--workbook`
  - Excel 文件路径。传入后会覆盖 `.config` 中的路径配置
- `--config`
  - `.config` 文件路径，默认仓库根目录下的 `.config`
- `--kconfig`
  - `Kconfig` 文件路径，默认 `Kconfig`
- `--output-dir`
  - 输出目录，默认 `output`
- `--header-template`
  - `.h` 模板路径，默认 `resources/templates/app_config.h.tpl`
- `--source-template`
  - `.c` 模板路径，默认 `resources/templates/app_config.c.tpl`
- `--animation-board-type-map`
  - 动画灯板映射 JSON，默认 `resources/animation_board_type_map.json`

### `scripts/extract_excel_json.py`

把 Excel 中已支持的 sheet 提取为 JSON。

默认命令：

```powershell
uv run python scripts/extract_excel_json.py
```

默认行为：

- 从 `.config` 读取 Excel 路径
- 如果 `.config` 不存在，则回退到 `Kconfig` 默认路径
- 自动转换工作簿中所有已支持的 sheet
- 默认输出到 `output/<sheet_name>.json`
- 匹配 sheet 名时会忽略首尾空格

参数：

```powershell
uv run python scripts/extract_excel_json.py --config <config路径> --workbook <excel路径> --sheet <sheet名> --output <json路径或目录>
```

- `--config`
  - `.config` 文件路径，默认仓库根目录下的 `.config`
- `--workbook`
  - Excel 文件路径。传入后会覆盖 `.config` 中的路径配置
- `--sheet`
  - 指定单个 sheet；不传则批量转换全部已支持 sheet
- `--output`
  - 指定单个 sheet 时为 JSON 文件路径；批量转换时为输出目录

常用示例：

```powershell
uv run python scripts/extract_excel_json.py
uv run python scripts/extract_excel_json.py --config configs\project_a.config
uv run python scripts/extract_excel_json.py --sheet HCM_PriLIN_Matrix --output output\hcm_prilin_matrix.json
uv run python scripts/extract_excel_json.py --sheet "Lock Mode1"
uv run python scripts/extract_excel_json.py --sheet current_config
uv run python scripts/extract_excel_json.py --output output\all_sheets
```

### `scripts/kconfig_to_json.py`

把 `Kconfig/.config` 转为 `Kconfig.json`。

默认命令：

```powershell
uv run python scripts/kconfig_to_json.py
```

参数：

```powershell
uv run python scripts/kconfig_to_json.py --kconfig <Kconfig路径> --config <.config路径> --output <json路径>
```

- `--kconfig`
  - `Kconfig` 文件路径，默认 `Kconfig`
- `--config`
  - `.config` 路径，默认仓库根目录下的 `.config`
- `--output`
  - 输出 JSON 路径，默认 `output/Kconfig.json`

### `scripts/build_render_context.py`

把 Excel JSON 和 `Kconfig.json` 合并为统一的渲染上下文。

默认命令：

```powershell
uv run python scripts/build_render_context.py
```

参数：

```powershell
uv run python scripts/build_render_context.py --input-dir <excel_json目录> --kconfig-json <kconfig.json> --output <render_context.json>
```

- `--input-dir`
  - Excel JSON 所在目录，默认 `output`
- `--kconfig-json`
  - Kconfig JSON 路径，默认 `output/Kconfig.json`
- `--header-template`
  - `.h` 模板路径，默认 `resources/templates/app_config.h.tpl`
- `--source-template`
  - `.c` 模板路径，默认 `resources/templates/app_config.c.tpl`
- `--output`
  - 输出路径，默认 `output/render_context.json`
- `--animation-board-type-map`
  - 动画灯板映射 JSON，默认 `resources/animation_board_type_map.json`

说明：

- 该步骤会优先生成模板可直接消费的标量占位符
- 还会生成模板使用的代码片段区块
- 对于暂未完成业务映射的大段 C 代码，当前会先落成 `TODO` 注释 stub
- `render_context.json` 的推荐结构可参考 [../resources/templates/README.md](../resources/templates/README.md)

### `scripts/render_app_config.py`

只负责渲染模板，不直接解析 Excel，也不直接理解 Kconfig。

默认命令：

```powershell
uv run python scripts/render_app_config.py --context output\render_context.json
```

参数：

```powershell
uv run python scripts/render_app_config.py --context <context.json> --header-template <h模板> --source-template <c模板> --header-output <输出h> --source-output <输出c>
```

- `--context`
  - 合并后的 render context JSON 路径，必填
- `--header-template`
  - `.h` 模板路径，默认 `resources/templates/app_config.h.tpl`
- `--source-template`
  - `.c` 模板路径，默认 `resources/templates/app_config.c.tpl`
- `--header-output`
  - 输出头文件路径，默认 `output/app_config.h`
- `--source-output`
  - 输出源文件路径，默认 `output/app_config.c`

## 输出结构约定

### 通用约定

- 所有输出 JSON 顶层都包含 `schema_version`
- 输出结构以“程序可直接消费”为目标，尽量避免同一类数据同时出现对象和数组两种形态
- `render_context.json` 会同时保留原始 `excel` / `kconfig` 数据，以及模板渲染需要的 `placeholders` / `sections`

### `HCM_PriLIN_Matrix`

每个配置项会统一整理成：

```json
{
  "schema_version": 2,
  "id": 12,
  "name": "日行灯降额配置",
  "entries": [
    {
      "value_1": 120,
      "value_2": 110,
      "value_3": 75
    }
  ]
}
```

约定：

- Excel 中 C、D、E 三列统一映射成 `value_1`、`value_2`、`value_3`
- 纯数字文本会优先转成数值类型
- `(default)` 标记会被移除
- 顶层还会提供 `items_by_id`，便于按配置项 ID 索引

### `CH_Cfg`

按 IC 号分组输出通道配置：

```json
{
  "schema_version": 2,
  "sheet_name": "CH_Cfg",
  "ic_count": 12,
  "channel_count": 111,
  "config_type_descriptions": {
    "0": "..."
  },
  "ics": {
    "IC0": {
      "CH00": 2,
      "CH01": 2
    }
  }
}
```

约定：

- 顶层 `ics` 以 `ICx` 为 key
- 每个 IC 内部通道统一使用 `CHyy`
- `config_type_descriptions` 会保留类型说明，便于后续映射

### `Lock ModeN` / `Unlock ModeN`

原始动画 sheet 会按帧输出左侧表格数据：

```json
{
  "schema_version": 2,
  "sheet_name": "Lock Mode1",
  "table_side": "left",
  "led_side": "right",
  "column_count": 54,
  "frame_count": 301,
  "columns": [
    {
      "column_id": 0,
      "section_name": "DRL/POS/ADS_R",
      "mapping_name": "IC500(1010)",
      "output_name": "OUT4\nDRL_POS_16",
      "led_name": "LED630、LED631"
    }
  ],
  "frames": [
    {
      "time_ms": 0,
      "values": [0, 0, 0, 100]
    }
  ]
}
```

约定：

- 只支持匹配 `Lock ModeN` / `Unlock ModeN` 的 sheet 名
- 当前只提取原表左侧动画区
- 左右区域之间的空列会自动跳过
- `frames[*].values` 与 `columns` 一一对应
- 模式数量直接由工作簿中存在的原始 sheet 数量决定

### `current_config`

按通道输出当前电流配置：

```json
{
  "schema_version": 2,
  "sheet_name": "current_config",
  "total_ic_count": 12,
  "channel_count_per_ic": 24,
  "channel_count": 288,
  "channels": {
    "IC0-CH00": {
      "k_factory": 100,
      "max_current_per_channel": 99,
      "primary_function": {
        "name": "DRL",
        "dimming_coefficient": 114,
        "total_coefficient": 114
      }
    }
  }
}
```

约定：

- 通道 key 统一为 `ICx-CHyy`
- 公式列会优先输出 Excel 缓存的计算结果，而不是原始公式字符串
- 当前渲染 `u8_cvcc_k_array` 时，会读取 `primary_function.dimming_coefficient`
- 如果缺少功能 1 或缺少调光系数，当前模板会按 `100` 回填

### `Motor_Cfg`

主要数据会收敛到 `motor_config` 下：

```json
{
  "schema_version": 2,
  "sheet_name": "Motor_Cfg",
  "title": "Leveling Stepper Motor Setting",
  "motor_config": {
    "safety_voltage": {
      "low_voltage_v": 9,
      "over_voltage_v": 16
    },
    "general_settings": {
      "positive_command_action": "Pull"
    },
    "control_modes": {
      "reference_run": {
        "running_current": 560
      }
    },
    "microstep_mode": "1/8[FS]",
    "positions": {
      "pos1": {
        "label": "Mechanical Block Downward"
      }
    },
    "afs_positions": {
      "level0": {
        "c_mode": 0,
        "v_mode": 0,
        "e_mode": 0
      }
    }
  }
}
```

约定：

- 自然语言字段名会整理成稳定的 `snake_case` key
- `positions`、`afs_positions` 会按稳定 ID 输出为对象
- 公式列同样优先输出 Excel 缓存结果

### `TI_sequential`

输出单个 PWM 动画的逐帧通道值：

```json
{
  "schema_version": 2,
  "sheet_name": "TI_sequential",
  "total_ic_count": 12,
  "channel_count_per_ic": 24,
  "animation_count": 1,
  "animation": {
    "channel_type": "PWM",
    "frames": [
      {
        "time_ms": 0,
        "channels": {
          "IC2-CH00": 0,
          "IC2-CH01": 0
        }
      }
    ]
  }
}
```

约定：

- 每一行都会被视为一帧
- 通道值放在 `animation.frames[*].channels`
- 当前实现中，值为 `0` 的通道不会写入 `channels`

## 注意事项

- 当前脚本已实现 `HCM_PriLIN_Matrix`、`CH_Cfg`、`current_config`、`Motor_Cfg`、`TI_sequential`，以及所有匹配 `Lock ModeN` / `Unlock ModeN` 的原始动画 sheet
- 如果动画里出现新的灯板名称，需要同步补充 `resources/animation_board_type_map.json`
- `xlsx/`、`output/`、`.config` 默认不会提交到 Git

## History

### 2026/04/02

1. 完成通道 type 0 - type 4 的配置
2. 清理模板文件

## TODO

- [ ] 整理替换数据来源
- [ ] 评估是否把 `CHCM_CFG_IDX_MAX` 改为 Kconfig 可配置项，用它动态控制 `CHCM` 尾部 `RESERVED` 数量
- [ ] 如果启用该方案，需要同时调整 `scripts/build_render_context.py`、`resources/templates/app_config.h.tpl` 和 `resources/templates/app_config.c.tpl`
- [ ] 预期方向是以前半段使用 Excel 实际 CFG 数量，后半段由 `CHCM_CFG_IDX_MAX` 推导 `RESERVED` 数量
- [ ] 当配置值小于 Excel 实际项数量时，脚本应直接报错

# chcm_config

当前仓库用于把 CHCM 配置数据拆成四个明确步骤：

- `extract_excel_json.py`: 把 Excel 中的 sheet 转成 JSON
- `kconfig_to_json.py`: 把 `Kconfig/.config` 转成 JSON
- `build_render_context.py`: 合并 Excel JSON 和 Kconfig JSON，生成 `render_context.json`
- `render_app_config.py`: 读取 `render_context.json`，渲染 `app_config.c/.h`
- `run_pipeline.py`: 按顺序自动执行以上完整转换流程

目前已支持的 sheet:

- `HCM_PriLIN_Matrix`
- `CH_Cfg`
- `Lock ModeN` / `Unlock ModeN`
- `current_config`
- `Motor_Cfg`
- `TI_sequential`

## Excel 路径配置

仓库新增了 `Kconfig`，可用来配置 Excel 文件路径。

配置优先级:

- 命令行 `--workbook`
- `.config` 中的 `CONFIG_CHCM_WORKBOOK_PATH`
- `Kconfig` 中的默认值

推荐做法:

```powershell
Copy-Item .config.example .config
```

然后编辑 `.config`:

```text
CONFIG_CHCM_WORKBOOK_PATH="xlsx/E01 CHCM-1C-2C1V(得邦)_config_Dataset_LEFT_V0.2.xlsx"
```

`.config` 已加入 `.gitignore`，不会被自动提交。

## 环境准备

仓库使用 `uv` 管理 Python 依赖。

```powershell
uv sync
```

## 脚本运行

当前支持两种运行方式：

- 一键执行完整流程
- 手动分步执行

### 一键执行完整流程

默认命令:

```powershell
uv run python run_pipeline.py
```

默认行为:

- 自动顺序执行 `extract_excel_json.py`
- 自动顺序执行 `kconfig_to_json.py`
- 自动顺序执行 `build_render_context.py`
- 自动顺序执行 `render_app_config.py`
- 默认输出到 `output/` 目录
- 默认生成 `output/render_context.json`
- 默认生成 `output/app_config.h`
- 默认生成 `output/app_config.c`

参数说明:

```powershell
uv run python run_pipeline.py --workbook <excel路径> --config <.config路径> --kconfig <Kconfig路径> --output-dir <输出目录>
```

- `--workbook`: Excel 文件路径。传入后会覆盖 `.config` 中的路径配置
- `--config`: Kconfig 生成的 `.config` 文件路径，默认是仓库根目录下的 `.config`
- `--kconfig`: `Kconfig` 文件路径，默认 `Kconfig`
- `--output-dir`: 输出目录，默认 `output`

### 手动分步执行

#### 第一步：Excel 转 JSON

默认命令:

```powershell
uv run python extract_excel_json.py
```

默认行为:

- 默认从 `.config` 读取 Excel 路径
- 如果 `.config` 不存在，则回退到 `Kconfig` 默认路径
- 默认转换工作簿中所有当前已支持的 sheet
- 默认输出到 `output/<sheet_name>.json`
- sheet 名匹配时会自动忽略首尾空格
- 默认输出精简结果，只保留配置项和实际值

参数说明:

```powershell
uv run python extract_excel_json.py --config <config路径> --workbook <excel路径> --sheet <sheet名> --output <json路径>
```

- `--config`: Kconfig 生成的 `.config` 文件路径，默认是仓库根目录下的 `.config`
- `--workbook`: Excel 文件路径。传入后会覆盖 `.config` 中的路径配置
- `--sheet`: sheet 名称。不传时会转换工作簿中所有当前已支持的 sheet
- `--output`: 指定单个 sheet 时为 JSON 文件路径；未指定 `--sheet` 且批量转换时为输出目录

## 常用示例

输出默认 JSON:

```powershell
uv run python extract_excel_json.py
```

使用自定义 `.config`:

```powershell
uv run python extract_excel_json.py --config configs\\project_a.config
```

指定输出路径:

```powershell
uv run python extract_excel_json.py --sheet HCM_PriLIN_Matrix --output output\\hcm_prilin_matrix.json
```

批量转换到自定义目录:

```powershell
uv run python extract_excel_json.py --output output\\all_sheets
```

转换 `CH_Cfg`:

```powershell
uv run python extract_excel_json.py --sheet CH_Cfg
```

转换 `Lock Mode1`:

```powershell
uv run python extract_excel_json.py --sheet "Lock Mode1"
```

转换 `Unlock Mode1`:

```powershell
uv run python extract_excel_json.py --sheet "Unlock Mode1"
```

转换 `current_config`:

```powershell
uv run python extract_excel_json.py --sheet current_config
```

转换 `Motor_Cfg`:

```powershell
uv run python extract_excel_json.py --sheet Motor_Cfg
```

转换 `TI_sequential`:

```powershell
uv run python extract_excel_json.py --sheet TI_sequential
```

#### 第二步：Kconfig 转 JSON

默认命令:

```powershell
uv run python kconfig_to_json.py
```

参数说明:

```powershell
uv run python kconfig_to_json.py --kconfig <Kconfig路径> --config <.config路径> --output <json路径>
```

- `--kconfig`: `Kconfig` 文件路径，默认 `Kconfig`
- `--config`: `.config` 路径，默认仓库根目录下的 `.config`
- `--output`: 输出 JSON 路径，默认 `output/Kconfig.json`

#### 第三步：生成 render_context.json

默认命令:

```powershell
uv run python build_render_context.py
```

参数说明:

```powershell
uv run python build_render_context.py --input-dir <excel_json目录> --kconfig-json <kconfig.json> --output <render_context.json>
```

- `--input-dir`: Excel JSON 所在目录，默认 `output`
- `--kconfig-json`: Kconfig JSON 路径，默认 `output/Kconfig.json`
- `--output`: 输出 render context 路径，默认 `output/render_context.json`

当前 `build_render_context.py` 会优先填充模板中能直接推导出来的标量占位符。
对于还没有完成业务映射的大段 C 代码块，占位符会先落成 `TODO` 注释 stub，方便后续逐步替换成真实生成逻辑。

#### 第四步：JSON 渲染 app_config

`render_app_config.py` 不直接解析 Excel，也不直接理解 Kconfig。
它只负责读取“已经合并好的 render context JSON”，然后渲染 [templates/app_config.h.tpl](templates/app_config.h.tpl) 和 [templates/app_config.c.tpl](templates/app_config.c.tpl)。

默认命令:

```powershell
uv run python render_app_config.py --context output\\render_context.json
```

参数说明:

```powershell
uv run python render_app_config.py --context <context.json> --header-template <h模板> --source-template <c模板> --header-output <输出h> --source-output <输出c>
```

- `--context`: 合并后的 render context JSON 路径，必填
- `--header-template`: `.h` 模板路径，默认 `templates/app_config.h.tpl`
- `--source-template`: `.c` 模板路径，默认 `templates/app_config.c.tpl`
- `--header-output`: 输出头文件路径，默认 `output/app_config.h`
- `--source-output`: 输出源文件路径，默认 `output/app_config.c`

`build_render_context.py` 生成的 `render_context.json` 会同时保留原始 `excel` / `kconfig` 数据，以及模板渲染用的 `placeholders` / `sections`。
render context JSON 推荐结构可参考 [templates/README.md](templates/README.md)。

## TODO

- 评估是否把 `CHCM_CFG_IDX_MAX` 改为 Kconfig 可配置项，用它动态控制 `CHCM` 尾部 `RESERVED` 数量。
- 如果启用这个方案，需要同时调整 `build_render_context.py`、`templates/app_config.h.tpl` 和 `templates/app_config.c.tpl`，不能只修改 `CHCM_CFG_IDX_MAX` 一个值。
- 这个动态逻辑会同时影响 `.h` 里的 `RESERVED` 宏数量，以及 `.c` 里的 `CHCM_Cfg[]` 数组长度和尾部 `reserved` 项数量。
- 预期方向是以 Excel 实际 CFG 数量作为前半段固定项，再由 `CHCM_CFG_IDX_MAX` 推导尾部 `RESERVED` 数量；当配置值小于 Excel 实际项数量时，脚本应直接报错。

## 当前输出格式

所有输出结果的顶层都会包含 `schema_version`，便于程序侧做格式兼容。

`HCM_PriLIN_Matrix` 每个配置项都会输出为:

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

说明:

- 配置项 `0` 也会被提取
- Excel 中 C、D、E 三列统一映射成 `value_1`、`value_2`、`value_3`
- 值中的 `(default)` 标记会被移除
- 如果某个配置项只用了部分列，只输出实际有值的字段
- 每个配置项统一使用 `entries` 数组，避免程序侧再区分对象和数组两种类型
- 纯数字文本会优先转换成数值类型，方便程序直接读取
- 顶层还会输出 `items_by_id`，便于程序直接按配置项 ID 索引

表格型配置项示例:

```json
{
  "schema_version": 2,
  "id": 17,
  "name": "直流电机四档电压值配置",
  "entries": [
    {
      "value_1": 0,
      "value_2": 57.8
    },
    {
      "value_1": 1,
      "value_2": 49.7
    }
  ]
}
```

`CH_Cfg` 会按 IC 号分组输出通道配置:

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

说明:

- 顶层 `ics` 以 `ICx` 为 key 分组，每组内部再用 `CHyy` 保存该 IC 的通道配置
- 通道名仍统一成 `CHyy` 格式，便于和 `Lock/Unlock ModeN`、`TI_sequential`、`current_config` 做映射
- 配置类型说明仍然保留在 `config_type_descriptions`

原始解闭锁动画 sheet（例如 `Lock Mode1`、`Unlock Mode1`）会按帧输出左侧表格数据:

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
    },
    {
      "time_ms": 10,
      "values": [0, 0, 0, 100]
    }
  ]
}
```

说明:

- sheet 名需要匹配 `Lock ModeN` / `Unlock ModeN`，其中 `N` 为模式号
- 当前只提取表格左侧动画区；这部分数据代表右侧 LED 动画
- 左右区域之间的空列会自动跳过，不会出现在 `columns` 中
- `columns` 保留列顺序和原始映射信息，`frames[*].values` 与 `columns` 一一对应
- `frame_count` 会在后续渲染阶段直接作为该模式的总步数来源
- `lock` / `unlock` 的模式数量也直接由存在的原始 sheet 数量决定，不再依赖 `Animation_Cfg`
`current_config` 会按通道输出当前电流配置:

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
      },
      "secondary_function": {
        "name": "PL",
        "dimming_coefficient": 68.57,
        "total_coefficient": 13.714
      }
    },
    "IC0-CH05": {
      "k_factory": 100,
      "max_current_per_channel": 99,
      "primary_function": {
        "name": "ADAS"
      },
      "fixed_current": 50
    }
  }
}
```

说明:

- 顶层会输出总 IC 数 `total_ic_count` 和每个 IC 的通道数 `channel_count_per_ic`
- 主要数据会放在 `channels` 下，并以 `ICx-CHyy` 作为 key，方便程序直接按通道索引
- 每个通道会按需要输出 `k_factory`、`max_current_per_channel`、`primary_function`、`fixed_current`、`secondary_function`
- 公式列会优先输出 Excel 缓存的计算结果，而不是原始公式字符串
- 当前渲染 `u8_cvcc_k_array` 时，会读取 `primary_function.dimming_coefficient`
- 如果某个通道没有功能 1 或没有调光系数，则该表项会按 `100` 回填
- 当前模板中 `u8_cvcc_k_array` 的声明使用 `USED_CVCC_CHIP_NUMS` 和 `USED_CVCC_CHANNEL_NUMS` 两个宏；当前物理维度固定为 `12x24`
`Motor_Cfg` 会拆成几个配置区块输出:

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
        "label": "Mechanical Block Downward",
        "steps_to_pos1_fs": 0,
        "spindle_distance_to_pos1_mm": 0,
        "wall_position_mm": -762.435789927779,
        "angle_deg": -4.36
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

说明:

- 主要数据都会收敛到 `motor_config` 下，便于程序侧统一处理
- 自然语言字段名会转换成稳定的 `snake_case` key
- `positions` 和 `afs_positions` 会按 `pos1`、`level0` 这样的稳定 ID 输出为对象，而不是数组
- `control_modes` 会按 `reference_run`、`normal_run` 这样的模式 key 分组
- `positions` 中的公式列会优先输出 Excel 缓存的计算结果，而不是原始公式字符串
- `microstep_mode` 目前保留 Excel 原值，例如 `1/8[FS]`
`TI_sequential` 会输出单个动画的逐帧 PWM 通道值:

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
      },
      {
        "time_ms": 10,
        "channels": {
          "IC2-CH00": 100,
          "IC2-CH01": 100
        }
      }
    ]
  }
}
```

说明:

- 顶层会输出总 IC 数 `total_ic_count` 和每个 IC 的通道数 `channel_count_per_ic`
- `TI_sequential` 会按单个动画输出到 `animation`
- 每一行都会被当作一帧，保留 `time_ms` 和该帧实际有值的通道 PWM
- 通道值为 `0` 时不会写入 `channels`
## 注意事项

- 当前脚本已实现 `HCM_PriLIN_Matrix`、`CH_Cfg`、`current_config`、`Motor_Cfg`、`TI_sequential`，以及所有匹配 `Lock ModeN` / `Unlock ModeN` 的原始动画 sheet；默认会把工作簿中存在的这些已支持 sheet 都转换出来
- `xlsx/` 和 `output/` 默认被 `.gitignore` 忽略，不会自动提交到 Git

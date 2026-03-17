# chcm_config

当前仓库用于把 CHCM 配置 Excel 中的 sheet 转成 JSON。

目前已支持的 sheet:

- `HCM_PriLIN_Matrix`
- `CH_Cfg`
- `Animation_Cfg`
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

默认命令:

```powershell
uv run python main.py
```

默认行为:

- 默认从 `.config` 读取 Excel 路径
- 如果 `.config` 不存在，则回退到 `Kconfig` 默认路径
- 默认转换工作簿中所有当前已支持的 sheet
- 默认输出到 `output/<sheet_name>.json`
- sheet 名匹配时会自动忽略首尾空格
- 默认输出精简结果，只保留配置项和实际值

## 参数说明

```powershell
uv run python main.py --config <config路径> --workbook <excel路径> --sheet <sheet名> --output <json路径> --mode <values|full>
```

- `--config`: Kconfig 生成的 `.config` 文件路径，默认是仓库根目录下的 `.config`
- `--workbook`: Excel 文件路径。传入后会覆盖 `.config` 中的路径配置
- `--sheet`: sheet 名称。不传时会转换工作簿中所有当前已支持的 sheet
- `--output`: 指定单个 sheet 时为 JSON 文件路径；未指定 `--sheet` 且批量转换时为输出目录
- `--mode values`: 精简模式。只输出配置项和值
- `--mode full`: 完整模式。输出解析后的完整中间结构，便于调试

## 常用示例

输出默认 JSON:

```powershell
uv run python main.py
```

使用自定义 `.config`:

```powershell
uv run python main.py --config configs\\project_a.config
```

指定输出路径:

```powershell
uv run python main.py --sheet HCM_PriLIN_Matrix --output output\\hcm_prilin_matrix_values.json
```

批量转换到自定义目录:

```powershell
uv run python main.py --output output\\all_sheets
```

转换 `CH_Cfg`:

```powershell
uv run python main.py --sheet CH_Cfg
```

转换 `Animation_Cfg`:

```powershell
uv run python main.py --sheet Animation_Cfg
```

转换 `current_config`:

```powershell
uv run python main.py --sheet current_config
```

转换 `Motor_Cfg`:

```powershell
uv run python main.py --sheet Motor_Cfg
```

转换 `TI_sequential`:

```powershell
uv run python main.py --sheet TI_sequential
```

查看完整解析结果:

```powershell
uv run python main.py --sheet HCM_PriLIN_Matrix --mode full --output output\\hcm_prilin_matrix_full.json
```

## 当前输出格式

`HCM_PriLIN_Matrix` 在 `values` 模式下，每个配置项都会输出为:

```json
{
  "id": 12,
  "name": "日行灯降额配置",
  "values": {
    "value_1": "120",
    "value_2": "110",
    "value_3": "75"
  }
}
```

说明:

- 配置项 `0` 也会被提取
- Excel 中 C、D、E 三列统一映射成 `value_1`、`value_2`、`value_3`
- 值中的 `(default)` 标记会被移除
- 如果某个配置项只用了部分列，只输出实际有值的字段
- 如果某个配置项本身是一组表格数据，`values` 会输出为数组

表格型配置项示例:

```json
{
  "id": 17,
  "name": "直流电机四档电压值配置",
  "values": [
    {
      "value_1": "0",
      "value_2": "57.8"
    },
    {
      "value_1": "1",
      "value_2": "49.7"
    }
  ]
}
```

`CH_Cfg` 在 `values` 模式下会输出配置类型说明和 12 个 IC 的通道配置:

```json
{
  "sheet_name": "CH_Cfg",
  "config_type_descriptions": {
    "0": "..."
  },
  "ics": [
    {
      "ic_name": "CV_IC0",
      "channels": {
        "CH0": 2,
        "CH1": 2
      }
    }
  ]
}
```

`Animation_Cfg` 在 `values` 模式下会按动画模式分组输出每一帧的 PWM 通道值:

```json
{
  "sheet_name": "Animation_Cfg",
  "total_ic_count": 12,
  "channel_count_per_ic": 24,
  "unlock_animation_count": 1,
  "lock_animation_count": 1,
  "unlock_animations": [
    {
      "mode_name": "unlock Mode 1",
      "channel_type": "PWM",
      "frames": [
        {
          "time_ms": 0,
          "channels": {
            "IC6-CH11": 100
          }
        },
        {
          "time_ms": 10,
          "channels": {
            "IC6-CH10": 100,
            "IC6-CH11": 100
          }
        }
      ]
    }
  ],
  "lock_animations": [
    {
      "mode_name": "lock Mode 1",
      "channel_type": "PWM",
      "frames": []
    }
  ]
}
```

说明:

- 顶层会额外输出总 IC 数 `total_ic_count` 和每个 IC 的通道数 `channel_count_per_ic`
- 顶层会额外输出 `unlock_animation_count` 和 `lock_animation_count`
- 动画会明确拆分到 `unlock_animations` 和 `lock_animations`，便于后续同类模式继续扩展
- 后续每一行都会被当作一帧，保留 `time_ms` 和该帧实际有值的通道 PWM
- 第 2 行 `K factory` 会被忽略，不会输出到 JSON
- 会自动忽略右侧不属于 `ICx-CHyy` 的备注列
- 如果后续出现既不是 `unlock` 也不是 `lock` 的模式，会额外输出到 `other_animations`
- `full` 模式下会额外保留 `animation_kind`、`source_row`、通道表头和分组行范围，便于调试

`current_config` 在 `values` 模式下会按通道输出当前电流配置:

```json
{
  "sheet_name": "current_config",
  "total_ic_count": 12,
  "channel_count_per_ic": 24,
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
- `full` 模式下会额外保留 `source_row`、表头名和公式字段，便于调试

`Motor_Cfg` 在 `values` 模式下会拆成几个配置区块输出:

```json
{
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
- `full` 模式下会额外保留 `source_row`、表头名，以及位置公式字段，便于调试

`TI_sequential` 在 `values` 模式下会输出单个动画的逐帧 PWM 通道值:

```json
{
  "sheet_name": "TI_sequential",
  "total_ic_count": 12,
  "channel_count_per_ic": 24,
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
- `full` 模式下会额外保留 `source_row`、通道表头和动画行范围，便于调试

## 注意事项

- 当前脚本已实现 `HCM_PriLIN_Matrix`、`CH_Cfg`、`Animation_Cfg`、`current_config`、`Motor_Cfg` 和 `TI_sequential` 的解析；默认会把工作簿中存在的这六个已支持 sheet 都转换出来
- `xlsx/` 和 `output/` 默认被 `.gitignore` 忽略，不会自动提交到 Git

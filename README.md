# chcm_config

当前仓库用于把 CHCM 配置 Excel 中的 sheet 转成 JSON。

目前已支持的 sheet:

- `HCM_PriLIN_Matrix`
- `CH_Cfg`

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
- 默认读取 sheet `HCM_PriLIN_Matrix`
- 默认输出到 `output/<sheet_name>.json`
- sheet 名匹配时会自动忽略首尾空格
- 默认输出精简结果，只保留配置项和实际值

## 参数说明

```powershell
uv run python main.py --config <config路径> --workbook <excel路径> --sheet <sheet名> --output <json路径> --mode <values|full>
```

- `--config`: Kconfig 生成的 `.config` 文件路径，默认是仓库根目录下的 `.config`
- `--workbook`: Excel 文件路径。传入后会覆盖 `.config` 中的路径配置
- `--sheet`: sheet 名称。当前仅支持 `HCM_PriLIN_Matrix`
- `--output`: 输出 JSON 文件路径
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
uv run python main.py --output output\\hcm_prilin_matrix_values.json
```

转换 `CH_Cfg`:

```powershell
uv run python main.py --sheet CH_Cfg
```

查看完整解析结果:

```powershell
uv run python main.py --mode full --output output\\hcm_prilin_matrix_full.json
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

## 注意事项

- 当前脚本已实现 `HCM_PriLIN_Matrix` 和 `CH_Cfg` 的解析
- `xlsx/` 和 `output/` 默认被 `.gitignore` 忽略，不会自动提交到 Git

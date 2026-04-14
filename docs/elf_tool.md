# elf_tool

`scripts/elf_tool.py` 用于读取 ELF 中的 `cflash` 相关符号，并提供以下两个子命令：

- `compare`：比较两个 ELF 在 `cflash` 范围内的命名符号地址是否一致
- `cflash-range`：读取指定 ELF 中的 `__cflash_start` 和 `__cflash_end`

脚本路径：

```text
chcm_config/scripts/elf_tool.py
```

默认使用的 `nm` 工具：

```text
D:\environment\windows\arm-gcc\arm-gnu-toolchain-12.3.rel1\bin\arm-none-eabi-nm.exe
```

如果本机工具链路径不同，可以通过 `--nm` 手动指定。

## 运行前提

当前 `chcm_config` 使用 `uv` 管理 Python 环境，建议在 `chcm_config` 目录下执行：

```powershell
uv run python scripts/elf_tool.py -h
```

## 命令总览

```powershell
uv run python scripts/elf_tool.py compare <reference_elf> <candidate_elf> [--detail] [--nm <path-to-arm-none-eabi-nm>]
uv run python scripts/elf_tool.py cflash-range <elf> [--nm <path-to-arm-none-eabi-nm>]
```

## cflash-range

`cflash-range` 用于读取指定 ELF 中的：

- `__cflash_start`
- `__cflash_end`

并计算两者之间的大小。

### 基本用法

```powershell
uv run python scripts/elf_tool.py cflash-range build\app_config.elf
```

### 示例输出

```text
elf: build\app_config.elf
__cflash_start = 0x00500000
__cflash_end   = 0x00508780
size           = 0x8780 (34688 bytes)
```

### 返回结果

- 成功时返回 `0`
- 如果 ELF 不存在、`nm` 不存在，或缺少 `__cflash_start` / `__cflash_end`，会直接报错退出

## compare

`compare` 用于比较两个 ELF 在 `cflash` 范围内的命名符号地址：

- `reference_elf`：通常是主工程生成的完整 ELF
- `candidate_elf`：通常是 `chcm_config` 单独生成的配置区 ELF

比较范围由两个 ELF 各自的 `__cflash_start` 和 `__cflash_end` 自动确定。

默认会忽略以下符号：

- 以 `.` 开头的名字
- 以 `$` 开头的名字

另外，比较结果会始终包含：

- `__cflash_start`
- `__cflash_end`

### 基本用法

```powershell
uv run python scripts/elf_tool.py compare ..\build\CHY_A_plus_plus.elf build\app_config.elf
```

### 显示全部比较明细

```powershell
uv run python scripts/elf_tool.py compare ..\build\CHY_A_plus_plus.elf build\app_config.elf --detail
```

### 输出说明

摘要部分会输出：

- `reference elf`
- `candidate elf`
- `reference cflash range`
- `candidate cflash range`
- `reference symbols in cflash`
- `candidate symbols in cflash`
- `result`

如果存在差异，还会继续输出：

- `missing in candidate`
- `extra in candidate`
- `address mismatches`

使用 `--detail` 时，会输出所有参与比较的符号，例如：

```text
detail:
  match    configHeaderInfo: reference=0x00500000 candidate=0x00500000
  match    g_communication_version: reference=0x00500100 candidate=0x00500100
  mismatch CHCM_Cfg: reference=0x005086AC candidate=0x00508700
```

### 返回码

- `0`：所有参与比较的 `cflash` 符号地址一致
- `1`：发现符号缺失、额外符号或地址不一致

## 常见用法

先查看 `chcm_config` 当前生成 ELF 的 `cflash` 范围：

```powershell
uv run python scripts/elf_tool.py cflash-range build\app_config.elf
```

再比较主工程 ELF 和 `chcm_config` ELF 的 `cflash` 符号：

```powershell
uv run python scripts/elf_tool.py compare ..\build\CHY_A_plus_plus.elf build\app_config.elf --detail
```

如果输出：

```text
result: all cflash symbol addresses match
```

说明当前参与比较的 `cflash` 命名符号地址一致。

## 注意事项

- 链接脚本中必须定义 `__cflash_start` 和 `__cflash_end`
- `compare` 检查的是 `cflash` 范围内的命名符号，不是整个 ELF 的所有 section
- 如果主工程和 `chcm_config` 的链接脚本、结构体布局、编译宏或对齐规则不同，即使源码看起来一致，也可能导致地址变化

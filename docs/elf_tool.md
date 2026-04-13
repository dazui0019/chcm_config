# elf_tool

`scripts/elf_tool.py` 用于检查 `ELF` 文件中和 `cflash` 配置区相关的地址信息，当前提供两个子命令：

- `compare`: 对比两个 `ELF` 在 `cflash` 范围内的符号地址是否一致
- `cflash-range`: 读取指定 `ELF` 的 `__cflash_start` 和 `__cflash_end`, **所以链接脚本中一定要有这两个符号**。

脚本位置：

```text
chcm_config/scripts/elf_tool.py
```

默认使用的 `nm` 工具：

```text
chcm_config/toolchain/mingw-w64-x86_64-arm-none-eabi/bin/arm-none-eabi-nm.exe
```

## 运行前提

当前 `chcm_config` 已经使用 `uv` 管理 Python 环境，推荐在 `chcm_config` 目录中运行：

```powershell
uv run python scripts/elf_tool.py -h
```

## 命令总览

```powershell
uv run python scripts/elf_tool.py compare <reference_elf> <candidate_elf> [--detail]
uv run python scripts/elf_tool.py cflash-range <elf>
```

## compare

`compare` 用来对比两个 `ELF` 在 `cflash` 范围内的命名符号地址。

适用场景：

- 主工程 `CMake` 生成完整 `ELF`
- `chcm_config` 单独生成配置区 `ELF`
- 需要确认 `app_config.bin` 烧入 `cflash` 后，配置区符号地址与主工程一致

默认比较范围：

```text
从两个 ELF 各自的 __cflash_start 和 __cflash_end 自动读取
```

默认会忽略：

- 以 `.` 开头的名字
- 以 `$` 开头的名字

### 基本用法

```powershell
uv run python scripts/elf_tool.py compare ..\build\CHY_A_plus_plus.elf build\app_config.elf
```

### 显示全部符号地址

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

当存在差异时，还会继续输出：

- `missing in candidate`
- `extra in candidate`
- `address mismatches`

使用 `--detail` 时，还会输出所有参与比较的符号，例如：

```text
detail:
  match    configHeaderInfo: reference=0x00500000 candidate=0x00500000
  match    g_communication_version: reference=0x00500100 candidate=0x00500100
  mismatch CHCM_Cfg: reference=0x005086AC candidate=0x00508700
```

### 返回码

- `0`: 地址一致
- `1`: 存在差异

## cflash-range

`cflash-range` 用来读取指定 `ELF` 中的：

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

## 常见用法

先看 `chcm_config` 当前生成的配置区范围：

```powershell
uv run python scripts/elf_tool.py cflash-range build\app_config.elf
```

再对比主工程 `ELF` 和 `chcm_config` `ELF` 的 `cflash` 符号：

```powershell
uv run python scripts/elf_tool.py compare ..\build\CHY_A_plus_plus.elf build\app_config.elf --detail
```

如果 `compare` 返回 `result: all cflash symbol addresses match`，就说明当前参与比较的 `cflash` 命名符号地址一致。

当前比较结果也包含：

- `__cflash_start`
- `__cflash_end`

## 注意事项

- `compare` 检查的是 `cflash` 范围内的命名符号地址，不是整个 `ELF` 的所有 section。
- 如果主工程和 `chcm_config` 的链接脚本、结构体布局、编译宏或对齐规则不同，即使源码看起来一致，也可能导致地址变化。
- 如果 `ELF` 中缺少 `__cflash_start` 或 `__cflash_end`，`cflash-range` 会直接报错退出。

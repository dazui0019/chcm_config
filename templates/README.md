# app_config templates

这两个模板是从参考版 `app_config.c/.h` 提炼出来的，目标不是手工维护，而是给统一渲染链路使用：

1. Excel 提取 JSON
2. Kconfig/.config 提取 JSON
3. 合并成一份渲染上下文
4. 渲染 `app_config.h.tpl` 和 `app_config.c.tpl`

## 设计原则

- `app_config.h.tpl` 以固定骨架为主，只把明显变化的值留成占位符。
- `app_config.c.tpl` 以整段 C 代码块占位符为主，避免在模板里堆太多循环和条件。
- 同一个配置项只保留一个数据来源。Excel 里已经有的项，不要再在 Kconfig JSON 里重复定义。

## 占位符约定

- 标量占位符使用 `@NAME@`，适合直接替换成单个值或单个宏名。
- 代码块占位符也使用 `@NAME@`，但内容应当是“已经格式化好的完整 C 片段”。
- 如果模板里已经保留了大括号、分号或 `#if/#endif`，对应代码块就不要再重复输出这些外层结构。

## 推荐的上下文分层

推荐不要让模板直接消费原始 Excel JSON 或原始 Kconfig JSON，而是先合并成一层更稳定的 render context，例如：

```json
{
  "project_name": "PROJECT_A_SMALL",
  "eea_x": "VERSION_V5",
  "system_com_verion": "VERSION_V5",
  "used_matrix_chip_nums": 3,
  "used_matrix_led_nums": 32,
  "used_cvcc_chip_nums": 11,
  "sections": {
    "base_parameter_config_definitions": "...",
    "lock_unlock_macros": "...",
    "parameter_config_extern_declarations": "...",
    "lock_unlock_animation_definitions": "...",
    "cvcc_and_channel_map_definitions": "...",
    "chcm_cfg_definition": "...",
    "matrix_definitions": "...",
    "welcome_definition": "...",
    "motor_config_definition": "...",
    "loudness_definition": "..."
  }
}
```

这样做的好处是：

- Excel 和 Kconfig 可以先按各自规则转 JSON。
- 合并规则只写在一处。
- 模板只关心最终要输出什么 C 代码，不关心数据来自哪个 sheet 或哪个 `CONFIG_`。

## app_config.h.tpl 的主要占位符

- 标量：
  - `@PROJECT_NAME@`
  - `@EEA_X@`
  - `@SYSTEM_COM_VERION@`
  - `@USED_MATRIX_CHIP_NUMS@`
  - `@USED_MATRIX_LED_NUMS@`
  - `@USED_CVCC_CHIP_NUMS@`
  - `@CVCC_OUTPUT_VOLTAGE_LEVELS@`
  - `@SIGNAL_LED_CURRENT_METHOD@`
  - `@TI_DRL_CURRENT_DERATE_METHOD@`
  - `@TI_USED_LED_NUMS@`
  - `@TI_USED_LED_NUMS_DATA_LENS@`
  - `@TI_SWEEP_CYCLE_TIME@`
  - `@TI_SWEEP_USER_STEP@`
  - `@TI_SWEEP_STEP_MAX@`
  - `@TI_SEEP_ANIMATION_MODE@`
- 代码块：
  - `@LOCK_UNLOCK_MACROS@`
  - `@CHANNEL_LED_COUNT_MACROS@`
  - `@PARAMETER_CONFIG_EXTERN_DECLARATIONS@`
  - `@CHCM_CFG_INDEX_DEFINITIONS@`
  - `@LOUDNESS_INDEX_DEFINITIONS@`
  - `@CHCM_AND_MATRIX_EXTERN_DECLARATIONS@`

## app_config.c.tpl 的主要占位符

- `@BASE_PARAMETER_CONFIG_DEFINITIONS@`
- `@TI_SWEEP_FRAME_DEFINITION@`
- `@TI_SWEEP_LED_K_MODE_0_DEFINITION@`
- `@TI_SWEEP_LED_K_MODE_1_DEFINITION@`
- `@TI_SWEEP_LED_K_MODE_2_DEFINITION@`
- `@LOCK_UNLOCK_ANIMATION_DEFINITIONS@`
- `@CVCC_AND_CHANNEL_MAP_DEFINITIONS@`
- `@CHCM_CFG_DEFINITION@`
- `@MATRIX_DEFINITIONS@`
- `@WELCOME_DEFINITION@`
- `@MOTOR_CONFIG_DEFINITION@`
- `@LOUDNESS_DEFINITION@`

## 后续接 JSON 时的建议

- 先把 Kconfig 补充项转成和 Excel 解析结果一样“稳定、无副作用”的 JSON。
- 再写一个合并步骤，把 Excel JSON 和 Kconfig JSON 收敛成 render context。
- 最后再做模板渲染，不要在渲染阶段再做业务判断。

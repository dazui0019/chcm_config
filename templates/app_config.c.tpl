

#include "app_config.h"

const __attribute__ ((used,used,section(".parameter_config_0"))) uint8_t g_communication_version = @SYSTEM_COM_VERION@;
const __attribute__ ((used,used,section(".parameter_config_1"))) uint8_t g_used_cvcc_ic_nums = USED_CVCC_CHIP_NUMS;
const __attribute__ ((used,used,section(".parameter_config_2"))) APP_Cvcc_Cfg_T App_cvcc_cfg_L[USED_CVCC_CHIP_NUMS] = {
    /** ic_addr,          ic_type,           ic_uartchn,       ic_io_sw_nums, ic_sw_mask,   ic_max_current */
    {  @CVCC_CFG_IC0_ADDR@U,   USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC0_USED_SWITCH@U,   @CVCC_CFG_IC0_SWITCH_MASK@U,  @CVCC_CFG_IC0_MAX_CURRENT@ },
    {  @CVCC_CFG_IC1_ADDR@U,   USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC1_USED_SWITCH@U,   @CVCC_CFG_IC1_SWITCH_MASK@U,  @CVCC_CFG_IC1_MAX_CURRENT@ },
    {  @CVCC_CFG_IC2_ADDR@U,   USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC2_USED_SWITCH@U,   @CVCC_CFG_IC2_SWITCH_MASK@U,  @CVCC_CFG_IC2_MAX_CURRENT@ },
    {  @CVCC_CFG_IC3_ADDR@U,   USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC3_USED_SWITCH@U,   @CVCC_CFG_IC3_SWITCH_MASK@U,  @CVCC_CFG_IC3_MAX_CURRENT@ },
    {  @CVCC_CFG_IC4_ADDR@U,   USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC4_USED_SWITCH@U,   @CVCC_CFG_IC4_SWITCH_MASK@U,  @CVCC_CFG_IC4_MAX_CURRENT@ },
    {  @CVCC_CFG_IC5_ADDR@U,   USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC5_USED_SWITCH@U,   @CVCC_CFG_IC5_SWITCH_MASK@U,  @CVCC_CFG_IC5_MAX_CURRENT@ },
    {  @CVCC_CFG_IC6_ADDR@U,   USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC6_USED_SWITCH@U,   @CVCC_CFG_IC6_SWITCH_MASK@U,  @CVCC_CFG_IC6_MAX_CURRENT@ },
    {  @CVCC_CFG_IC7_ADDR@U,   USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC7_USED_SWITCH@U,   @CVCC_CFG_IC7_SWITCH_MASK@U,  @CVCC_CFG_IC7_MAX_CURRENT@ },
    {  @CVCC_CFG_IC8_ADDR@U,   USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC8_USED_SWITCH@U,   @CVCC_CFG_IC8_SWITCH_MASK@U,  @CVCC_CFG_IC8_MAX_CURRENT@ },
    {  @CVCC_CFG_IC9_ADDR@U,   USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC9_USED_SWITCH@U,   @CVCC_CFG_IC9_SWITCH_MASK@U,  @CVCC_CFG_IC9_MAX_CURRENT@ },
    {  @CVCC_CFG_IC10_ADDR@U,  USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC10_USED_SWITCH@U,  @CVCC_CFG_IC10_SWITCH_MASK@U, @CVCC_CFG_IC10_MAX_CURRENT@ },
    {  @CVCC_CFG_IC11_ADDR@U,  USED_CVCC_IC_TYPE,     USED_CVCC_UARTCHN,     @CVCC_CFG_IC11_USED_SWITCH@U,  @CVCC_CFG_IC11_SWITCH_MASK@U, @CVCC_CFG_IC11_MAX_CURRENT@ },
};

/* CVCC输出电压表: 使用CVCC_OUTPUT_VOLTAGE_IDX_xVx访问，表项值为对应目标电压的BUCK寄存器码值。 */
const __attribute__ ((used,used,section(".parameter_config_3"))) uint8_t g_cvcc_out_voltage_table[CVCC_OUTPUT_VOLTAGE_LEVELS] = {
    [CVCC_OUTPUT_VOLTAGE_IDX_5V0] = @CVCC_OUTPUT_VOLTAGE_5V0@U, // target 5.0V
    [CVCC_OUTPUT_VOLTAGE_IDX_5V2] = @CVCC_OUTPUT_VOLTAGE_5V2@U, // target 5.2V
    [CVCC_OUTPUT_VOLTAGE_IDX_5V4] = @CVCC_OUTPUT_VOLTAGE_5V4@U, // target 5.4V
    [CVCC_OUTPUT_VOLTAGE_IDX_5V6] = @CVCC_OUTPUT_VOLTAGE_5V6@U, // target 5.6V
    [CVCC_OUTPUT_VOLTAGE_IDX_5V8] = @CVCC_OUTPUT_VOLTAGE_5V8@U, // target 5.8V
    [CVCC_OUTPUT_VOLTAGE_IDX_6V0] = @CVCC_OUTPUT_VOLTAGE_6V0@U, // target 6.0V
    [CVCC_OUTPUT_VOLTAGE_IDX_6V2] = @CVCC_OUTPUT_VOLTAGE_6V2@U, // target 6.2V
    [CVCC_OUTPUT_VOLTAGE_IDX_6V4] = @CVCC_OUTPUT_VOLTAGE_6V4@U, // target 6.4V
    [CVCC_OUTPUT_VOLTAGE_IDX_6V6] = @CVCC_OUTPUT_VOLTAGE_6V6@U, // target 6.6V
    [CVCC_OUTPUT_VOLTAGE_IDX_6V8] = @CVCC_OUTPUT_VOLTAGE_6V8@U, // target 6.8V
    [CVCC_OUTPUT_VOLTAGE_IDX_7V0] = @CVCC_OUTPUT_VOLTAGE_7V0@U, // target 7.0V
    [CVCC_OUTPUT_VOLTAGE_IDX_7V2] = @CVCC_OUTPUT_VOLTAGE_7V2@U, // target 7.2V
    [CVCC_OUTPUT_VOLTAGE_IDX_7V4] = @CVCC_OUTPUT_VOLTAGE_7V4@U, // target 7.4V
    [CVCC_OUTPUT_VOLTAGE_IDX_7V6] = @CVCC_OUTPUT_VOLTAGE_7V6@U, // target 7.6V
    [CVCC_OUTPUT_VOLTAGE_IDX_7V8] = @CVCC_OUTPUT_VOLTAGE_7V8@U, // target 7.8V
    [CVCC_OUTPUT_VOLTAGE_IDX_8V0] = @CVCC_OUTPUT_VOLTAGE_8V0@U, // target 8.0V
    [CVCC_OUTPUT_VOLTAGE_IDX_8V2] = @CVCC_OUTPUT_VOLTAGE_8V2@U, // target 8.2V
    [CVCC_OUTPUT_VOLTAGE_IDX_8V4] = @CVCC_OUTPUT_VOLTAGE_8V4@U, // target 8.4V
};

/**< TI 流水动画, 每步每个led灯珠占空比(基于TI原始占空比) */
const __attribute__ ((used,used,section(".parameter_config_4"))) uint8_t u8_ti_sweep_led_nums = TI_USED_LED_NUMS;/**< Number of used LEDs */
const __attribute__ ((used,used,section(".parameter_config_5"))) uint8_t u8_ti_sweep_led_k[TI_SWEEP_USER_STEP + 1u][TI_USED_LED_NUMS] = {
/**<   @TI_SWEEP_LED_K_HEADER@ */
@TI_SWEEP_LED_K_ROWS@
};

/**< Config 1 Signale LED 解闭锁动画控制表格 */
const __attribute__ ((used,used,section(".parameter_config_6"))) uint16_t u8_lock_unlock_animation_total_steps[LOCK_UNLOCK_MAX_MODE_NUMS] = {
@LOCK_UNLOCK_ANIMATION_TOTAL_STEPS_ROWS@
};

const __attribute__ ((used,used,section(".parameter_config_7"))) uint8_t u8_lock_mode_type_nums = @LOCK_MODE_TYPE_NUMS@u;
const __attribute__ ((used,used,section(".parameter_config_8"))) uint8_t u8_unlock_mode_type_nums = @UNLOCK_MODE_TYPE_NUMS@u;

/**< Config 1 LOCK MODE1 DATA */
const __attribute__ ((used,used,section(".parameter_config_9")))  uint8_t u8_lock_mode1_animation[LOCK_MODE1_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS] = {
/**<  @LOCK_MODE1_ANIMATION_HEADER@ */
@LOCK_MODE1_ANIMATION_ROWS@
};

const __attribute__ ((used,used,section(".parameter_config_10")))  uint8_t u8_lock_mode2_animation[LOCK_MODE2_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS] = {
@LOCK_MODE2_ANIMATION_BODY@
};

const __attribute__ ((used,used,section(".parameter_config_11")))  uint8_t u8_lock_mode3_animation[LOCK_MODE3_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS] = {
@LOCK_MODE3_ANIMATION_BODY@
};

const __attribute__ ((used,used,section(".parameter_config_12")))  uint8_t u8_lock_mode4_animation[LOCK_MODE4_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS] = {
@LOCK_MODE4_ANIMATION_BODY@
};

const __attribute__ ((used,used,section(".parameter_config_13")))  uint8_t u8_lock_mode5_animation[LOCK_MODE5_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS] = {
@LOCK_MODE5_ANIMATION_BODY@
};

const __attribute__ ((used,used,section(".parameter_config_14")))  uint8_t u8_unlock_mode1_animation[UNLOCK_MODE1_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS] = {
/**<  @UNLOCK_MODE1_ANIMATION_HEADER@ */
@UNLOCK_MODE1_ANIMATION_ROWS@
};

const __attribute__ ((used,used,section(".parameter_config_15")))  uint8_t u8_unlock_mode2_animation[UNLOCK_MODE2_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS] = {
@UNLOCK_MODE2_ANIMATION_BODY@
};

const __attribute__ ((used,used,section(".parameter_config_16")))  uint8_t u8_unlock_mode3_animation[UNLOCK_MODE3_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS] = {
@UNLOCK_MODE3_ANIMATION_BODY@
};

const __attribute__ ((used,used,section(".parameter_config_17")))  uint8_t u8_unlock_mode4_animation[UNLOCK_MODE4_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS] = {
@UNLOCK_MODE4_ANIMATION_BODY@
};

const __attribute__ ((used,used,section(".parameter_config_18")))  uint8_t u8_unlock_mode5_animation[UNLOCK_MODE5_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS] = {
@UNLOCK_MODE5_ANIMATION_BODY@
};

/* 各恒流芯片每个通道输出电流值K系数 */
const __attribute__ ((used,used,section(".parameter_config_19")))  uint8_t u8_cvcc_k_array[USED_CVCC_CHIP_NUMS][USED_CVCC_CHANNEL_NUMS] = { 
@CVCC_K_ARRAY_ROWS@
};

// type 5: DRL单独通道，在TI点亮且有DRL使能时，DRL需要关闭；无TI使能时，按照DRL指令点灯
const __attribute__ ((used,used,section(".parameter_config_20")))  uint8_t u8_drl_0_cvcc_map_array[@CH_CFG_TYPE5_CVCC_MAP_ARRAY_SIZE@][2] = { 
@CH_CFG_TYPE5_CVCC_MAP_ROWS@
};
const __attribute__ ((used,used,section(".parameter_config_21")))  uint8_t u8_drl_0_cvcc_map_nums = @CH_CFG_TYPE5_CVCC_MAP_NUMS@U;
const __attribute__ ((used,used,section(".parameter_config_22")))  uint8_t u8_drl_0_unlock_lock_offset = @CH_CFG_TYPE5_UNLOCK_LOCK_OFFSET@U;

// type 6: DRL单独通道，在TI点亮且有DRL使能时，DRL需要降至PL亮度；无TI使能时，按照DRL指令点灯
const __attribute__ ((used,used,section(".parameter_config_23")))  uint8_t u8_drl_1_cvcc_map_array[@CH_CFG_TYPE6_CVCC_MAP_ARRAY_SIZE@][2] = { 
@CH_CFG_TYPE6_CVCC_MAP_ROWS@
};
const __attribute__ ((used,used,section(".parameter_config_24")))  uint8_t u8_drl_1_cvcc_map_nums = @CH_CFG_TYPE6_CVCC_MAP_NUMS@U;
const __attribute__ ((used,used,section(".parameter_config_25")))  uint8_t u8_drl_1_unlock_lock_offset = @CH_CFG_TYPE6_UNLOCK_LOCK_OFFSET@U;

// type 7: DRL单独通道，按照DRL点灯指令点亮
const __attribute__ ((used,used,section(".parameter_config_26")))  uint8_t u8_drl_2_cvcc_map_array[@CH_CFG_TYPE7_CVCC_MAP_ARRAY_SIZE@][2] = { 
@CH_CFG_TYPE7_CVCC_MAP_ROWS@
};
const __attribute__ ((used,used,section(".parameter_config_27")))  uint8_t u8_drl_2_cvcc_map_nums = @CH_CFG_TYPE7_CVCC_MAP_NUMS@U;
const __attribute__ ((used,used,section(".parameter_config_28")))  uint8_t u8_drl_2_unlock_lock_offset = @CH_CFG_TYPE7_UNLOCK_LOCK_OFFSET@U;

// type 2: DRL/PL共用通道，在TI使能且有DRL/PL使能时，DRL/PL需要关闭；在无TI使能时，按照PL＞DRL进行点灯
const __attribute__ ((used,used,section(".parameter_config_29")))  uint8_t u8_drl_pl_0_cvcc_map_array[@CH_CFG_TYPE2_CVCC_MAP_ARRAY_SIZE@][2] = { 
@CH_CFG_TYPE2_CVCC_MAP_ROWS@
};
const __attribute__ ((used,used,section(".parameter_config_30")))  uint8_t u8_drl_pl_0_cvcc_map_nums = @CH_CFG_TYPE2_CVCC_MAP_NUMS@U;
const __attribute__ ((used,used,section(".parameter_config_31")))  uint8_t u8_drl_pl_0_pl_duty = @CHCM_CFG_ITEM_11_WORD1@U;
const __attribute__ ((used,used,section(".parameter_config_32")))  uint8_t u8_drl_pl_0_unlock_lock_offset = @CH_CFG_TYPE2_UNLOCK_LOCK_OFFSET@U;

// type 3: DRL/PL共用通道，在TI使能且有DRL/PL使能时，DRL/PL需要降至PL亮度；在无TI使能时，按照PL＞DRL进行点灯
const __attribute__ ((used,used,section(".parameter_config_33")))  uint8_t u8_drl_pl_1_cvcc_map_array[@CH_CFG_TYPE3_CVCC_MAP_ARRAY_SIZE@][2] = { 
@CH_CFG_TYPE3_CVCC_MAP_ROWS@
};
const __attribute__ ((used,used,section(".parameter_config_34")))  uint8_t u8_drl_pl_1_cvcc_map_nums = @CH_CFG_TYPE3_CVCC_MAP_NUMS@U;
const __attribute__ ((used,used,section(".parameter_config_35")))  uint8_t u8_drl_pl_1_pl_duty = @CHCM_CFG_ITEM_11_WORD1@U;
const __attribute__ ((used,used,section(".parameter_config_36")))  uint8_t u8_drl_pl_1_unlock_lock_offset = @CH_CFG_TYPE3_UNLOCK_LOCK_OFFSET@U;

// type 4: DRL/PL共用通道，TI使能且有DRL/PL使能时，依照PL＞DRL优先级判断点亮灯光
const __attribute__ ((used,used,section(".parameter_config_37")))  uint8_t u8_drl_pl_2_cvcc_map_array[@CH_CFG_TYPE4_CVCC_MAP_ARRAY_SIZE@][2] = { 
@CH_CFG_TYPE4_CVCC_MAP_ROWS@
};
const __attribute__ ((used,used,section(".parameter_config_38")))  uint8_t u8_drl_pl_2_cvcc_map_nums = @CH_CFG_TYPE4_CVCC_MAP_NUMS@U;
const __attribute__ ((used,used,section(".parameter_config_39")))  uint8_t u8_drl_pl_2_pl_duty = @CHCM_CFG_ITEM_11_WORD1@U;
const __attribute__ ((used,used,section(".parameter_config_40")))  uint8_t u8_drl_pl_2_unlock_lock_offset = @CH_CFG_TYPE4_UNLOCK_LOCK_OFFSET@U;

const __attribute__ ((used,used,section(".parameter_config_41")))  uint8_t u8_hb_adb_mode = 0U; // 配置当前HB是否为ADB模式

// 特殊的pl通道, 保留原格式
const __attribute__ ((used,used,section(".parameter_config_42")))  uint8_t u8_pl_0_cvcc_map_array[2][2] = { { 0U, 0U }, { 0U, 0U } };
const __attribute__ ((used,used,section(".parameter_config_43")))  uint8_t u8_pl_0_cvcc_map_nums = 0U;
const __attribute__ ((used,used,section(".parameter_config_44")))  uint8_t u8_pl_0_unlock_lock_offset = @PL_0_UNLOCK_LOCK_OFFSET@U;

// type 8: PL单独通道，按照PL点灯指令点亮
const __attribute__ ((used,used,section(".parameter_config_45")))  uint8_t u8_pl_cvcc_map_array[@CH_CFG_TYPE8_CVCC_MAP_ARRAY_SIZE@][2] = 
{ 
@CH_CFG_TYPE8_CVCC_MAP_ROWS@
};
const __attribute__ ((used,used,section(".parameter_config_46")))  uint8_t u8_pl_cvcc_map_nums = @CH_CFG_TYPE8_CVCC_MAP_NUMS@U;
const __attribute__ ((used,used,section(".parameter_config_47")))  uint8_t u8_pl_cvcc_current = @CH_CFG_TYPE8_FIXED_CURRENT@U;
const __attribute__ ((used,used,section(".parameter_config_48")))  uint8_t u8_pl_unlock_lock_offset = @CH_CFG_TYPE8_UNLOCK_LOCK_OFFSET@U;
const __attribute__ ((used,used,section(".parameter_config_49")))  uint8_t u8_pl_duty_cfg = @CHCM_CFG_ITEM_11_WORD1@U;

// type 1: TI单独通道，当TI使能=1时，点亮该通道
const __attribute__ ((used,used,section(".parameter_config_50")))  uint8_t u8_ti_cvcc_map_array[@CH_CFG_TYPE1_CVCC_MAP_ARRAY_SIZE@][2] = { 
@CH_CFG_TYPE1_CVCC_MAP_ROWS@
};
const __attribute__ ((used,used,section(".parameter_config_51")))  uint8_t u8_ti_cvcc_map_nums = @CH_CFG_TYPE1_CVCC_MAP_NUMS@U;

// type 0: TI/DRL/PL共用通道，一个时刻只能点亮一个功能，遵照TI＞PL＞DRL进行点灯
const __attribute__ ((used,used,section(".parameter_config_52")))  uint8_t u8_ti_drl_pl_cvcc_map_array[@CH_CFG_TYPE0_CVCC_MAP_ARRAY_SIZE@][2] = { 
@CH_CFG_TYPE0_CVCC_MAP_ROWS@
};
const __attribute__ ((used,used,section(".parameter_config_53")))  uint8_t u8_ti_drl_pl_cvcc_map_nums = @CH_CFG_TYPE0_CVCC_MAP_NUMS@U;
const __attribute__ ((used,used,section(".parameter_config_54")))  uint8_t u8_ti_drl_pl_unlock_lock_offset = @CH_CFG_TYPE0_UNLOCK_LOCK_OFFSET@U;


// type 9: ADAS
const __attribute__ ((used,used,section(".parameter_config_55")))  uint8_t u8_adas_cvcc_map_array[@CH_CFG_TYPE9_CVCC_MAP_ARRAY_SIZE@][2] = 
{ 
@CH_CFG_TYPE9_CVCC_MAP_ROWS@
};
const __attribute__ ((used,used,section(".parameter_config_56")))  uint8_t u8_adas_cvcc_map_nums = @CH_CFG_TYPE9_CVCC_MAP_NUMS@U;
const __attribute__ ((used,used,section(".parameter_config_57")))  uint8_t u8_adas_cvcc_current = @CH_CFG_TYPE9_FIXED_CURRENT@U;

const __attribute__ ((used,used,section(".parameter_config_58")))  uint8_t u8_ti_drl_current_method = 1U;

const __attribute__ ((used,used,section(".parameter_config_59")))  uint8_t u8_drl_ntc_default_derate = 100U;

#if 1
const __attribute__ ((used,used,section(".parameter_config_61")))  CHCM_Cfg_T CHCM_Cfg[CHCM_CFG_IDX_MAX] = {
    {@CHCM_CFG_ITEM_0_WORD0@U, @CHCM_CFG_ITEM_0_WORD1@U, @CHCM_CFG_ITEM_0_WORD2@U}, /**< @CHCM_CFG_ITEM_0_COMMENT@ */
    {@CHCM_CFG_ITEM_1_WORD0@U, @CHCM_CFG_ITEM_1_WORD1@U, @CHCM_CFG_ITEM_1_WORD2@U}, /**< @CHCM_CFG_ITEM_1_COMMENT@ */
    {@CHCM_CFG_ITEM_2_WORD0@U, @CHCM_CFG_ITEM_2_WORD1@U, @CHCM_CFG_ITEM_2_WORD2@U}, /**< @CHCM_CFG_ITEM_2_COMMENT@ */
    {@CHCM_CFG_ITEM_3_WORD0@U, @CHCM_CFG_ITEM_3_WORD1@U, @CHCM_CFG_ITEM_3_WORD2@U}, /**< @CHCM_CFG_ITEM_3_COMMENT@ */
    {@CHCM_CFG_ITEM_4_WORD0@U, @CHCM_CFG_ITEM_4_WORD1@U, @CHCM_CFG_ITEM_4_WORD2@U}, /**< @CHCM_CFG_ITEM_4_COMMENT@ */
    {@CHCM_CFG_ITEM_5_WORD0@U, @CHCM_CFG_ITEM_5_WORD1@U, @CHCM_CFG_ITEM_5_WORD2@U}, /**< @CHCM_CFG_ITEM_5_COMMENT@ */
    {@CHCM_CFG_ITEM_6_WORD0@U, @CHCM_CFG_ITEM_6_WORD1@U, @CHCM_CFG_ITEM_6_WORD2@U}, /**< @CHCM_CFG_ITEM_6_COMMENT@ */
    {@CHCM_CFG_ITEM_7_WORD0@U, @CHCM_CFG_ITEM_7_WORD1@U, @CHCM_CFG_ITEM_7_WORD2@U}, /**< @CHCM_CFG_ITEM_7_COMMENT@ */
    {@CHCM_CFG_ITEM_8_WORD0@U, @CHCM_CFG_ITEM_8_WORD1@U, @CHCM_CFG_ITEM_8_WORD2@U}, /**< @CHCM_CFG_ITEM_8_COMMENT@ */
    {@CHCM_CFG_ITEM_9_WORD0@U, @CHCM_CFG_ITEM_9_WORD1@U, @CHCM_CFG_ITEM_9_WORD2@U}, /**< @CHCM_CFG_ITEM_9_COMMENT@ */
    {@CHCM_CFG_ITEM_10_WORD0@U, @CHCM_CFG_ITEM_10_WORD1@U, @CHCM_CFG_ITEM_10_WORD2@U}, /**< @CHCM_CFG_ITEM_10_COMMENT@ */
    {@CHCM_CFG_ITEM_11_WORD0@U, @CHCM_CFG_ITEM_11_WORD1@U, @CHCM_CFG_ITEM_11_WORD2@U}, /**< @CHCM_CFG_ITEM_11_COMMENT@ */
    {@CHCM_CFG_ITEM_12_WORD0@U, @CHCM_CFG_ITEM_12_WORD1@U, @CHCM_CFG_ITEM_12_WORD2@U}, /**< @CHCM_CFG_ITEM_12_COMMENT@ */
    {@CHCM_CFG_ITEM_13_WORD0@U, @CHCM_CFG_ITEM_13_WORD1@U, @CHCM_CFG_ITEM_13_WORD2@U}, /**< @CHCM_CFG_ITEM_13_COMMENT@ */
    {@CHCM_CFG_ITEM_14_WORD0@U, @CHCM_CFG_ITEM_14_WORD1@U, @CHCM_CFG_ITEM_14_WORD2@U}, /**< @CHCM_CFG_ITEM_14_COMMENT@ */
    {@CHCM_CFG_ITEM_15_WORD0@U, @CHCM_CFG_ITEM_15_WORD1@U, @CHCM_CFG_ITEM_15_WORD2@U}, /**< @CHCM_CFG_ITEM_15_COMMENT@ */
    {@CHCM_CFG_ITEM_16_WORD0@U, @CHCM_CFG_ITEM_16_WORD1@U, @CHCM_CFG_ITEM_16_WORD2@U}, /**< @CHCM_CFG_ITEM_16_COMMENT@ */
    {@CHCM_CFG_ITEM_17_WORD0@U, @CHCM_CFG_ITEM_17_WORD1@U, @CHCM_CFG_ITEM_17_WORD2@U}, /**< @CHCM_CFG_ITEM_17_COMMENT@ */
    {@CHCM_CFG_ITEM_18_WORD0@U, @CHCM_CFG_ITEM_18_WORD1@U, @CHCM_CFG_ITEM_18_WORD2@U}, /**< @CHCM_CFG_ITEM_18_COMMENT@ */
    {@CHCM_CFG_ITEM_19_WORD0@U, @CHCM_CFG_ITEM_19_WORD1@U, @CHCM_CFG_ITEM_19_WORD2@U}, /**< @CHCM_CFG_ITEM_19_COMMENT@ */
    {@CHCM_CFG_ITEM_20_WORD0@U, @CHCM_CFG_ITEM_20_WORD1@U, @CHCM_CFG_ITEM_20_WORD2@U}, /**< @CHCM_CFG_ITEM_20_COMMENT@ */
    {@CHCM_CFG_ITEM_21_WORD0@U, @CHCM_CFG_ITEM_21_WORD1@U, @CHCM_CFG_ITEM_21_WORD2@U}, /**< @CHCM_CFG_ITEM_21_COMMENT@ */
    {@CHCM_CFG_ITEM_22_WORD0@U, @CHCM_CFG_ITEM_22_WORD1@U, @CHCM_CFG_ITEM_22_WORD2@U}, /**< @CHCM_CFG_ITEM_22_COMMENT@ */
    {@CHCM_CFG_ITEM_23_WORD0@U, @CHCM_CFG_ITEM_23_WORD1@U, @CHCM_CFG_ITEM_23_WORD2@U}, /**< @CHCM_CFG_ITEM_23_COMMENT@ */
    {@CHCM_CFG_ITEM_24_WORD0@U, @CHCM_CFG_ITEM_24_WORD1@U, @CHCM_CFG_ITEM_24_WORD2@U}, /**< @CHCM_CFG_ITEM_24_COMMENT@ */
    {@CHCM_CFG_ITEM_25_WORD0@U, @CHCM_CFG_ITEM_25_WORD1@U, @CHCM_CFG_ITEM_25_WORD2@U}, /**< @CHCM_CFG_ITEM_25_COMMENT@ */
    {@CHCM_CFG_ITEM_26_WORD0@U, @CHCM_CFG_ITEM_26_WORD1@U, @CHCM_CFG_ITEM_26_WORD2@U}, /**< @CHCM_CFG_ITEM_26_COMMENT@ */
};

#if ( USED_MATRIX_FUNCTION == 1U )
const __attribute__ ((used,used,section(".parameter_config_49"))) uint8_t g_used_matrix_ic_nums = USED_MATRIX_CHIP_NUMS;
const __attribute__ ((used,used,section(".parameter_config_50")))APP_Matrix_Cfg_T App_matrix_cfg_L[USED_MATRIX_CHIP_NUMS] = {
               /** Matrix IC addr,  Matrix IC type,      used_uartchn,     Used switch,   switch_mask */     
   /**  IC0 */ {               0U,MATRIX_TPS92662A,     SUB_UARTCAN_2,          12U,        0x0fffU },
   /**  IC1 */ {               1U,MATRIX_TPS92662A,     SUB_UARTCAN_2,          12U,        0x0fffU },
   /**  IC2 */ {               2U,MATRIX_TPS92662A,     SUB_UARTCAN_2,           8U,        0x00ffU },
};

const __attribute__ ((used,used,section(".parameter_config_51"))) uint8_t g_used_matrix_led_nums = USED_MATRIX_LED_NUMS;

const __attribute__ ((used,used,section(".parameter_config_52"))) APP_ADB_LED_POS_Cfg_T g_used_matrix_led_id[USED_MATRIX_CHIP_NUMS][16U] = {
    {
        {0x00U,  0x00U},/**< matrix led 1  */
        {0x00U,  0x01U},/**< matrix led 2  */
        {0x00U,  0x02U},/**< matrix led 3  */
        {0x00U,  0x03U},/**< matrix led 4  */
        {0x00U,  0x04U},/**< matrix led 5  */
        {0x00U,  0x05U},/**< matrix led 6  */
        {0x00U,  0x06U},/**< matrix led 7  */
        {0x00U,  0x07U},/**< matrix led 8  */
        {0x00U,  0x08U},/**< matrix led 9  */
        {0x00U,  0x09U},/**< matrix led 10 */
        {0x00U,  0x10U},/**< matrix led 11 */
        {0x00U,  0x11U},/**< matrix led 12 */
        {0xffU,  0xffU},/**< not used */
        {0xffU,  0xffU},/**< not used */
        {0xffU,  0xffU},/**< not used */
        {0xffU,  0xffU},/**< not used */
    },
    {
        {0x01U,  0x00U},/**< matrix led 13 */
        {0x01U,  0x01U},/**< matrix led 14 */
        {0x01U,  0x02U},/**< matrix led 15 */
        {0x01U,  0x03U},/**< matrix led 16 */
        {0x01U,  0x04U},/**< matrix led 17 */
        {0x01U,  0x05U},/**< matrix led 18 */
        {0x01U,  0x06U},/**< matrix led 19 */
        {0x01U,  0x07U},/**< matrix led 20 */
        {0x01U,  0x08U},/**< matrix led 21 */
        {0x01U,  0x09U},/**< matrix led 22 */
        {0x01U,  0x10U},/**< matrix led 23 */
        {0x01U,  0x11U},/**< matrix led 24 */
        {0xffU,  0xffU},/**< not used */
        {0xffU,  0xffU},/**< not used */
        {0xffU,  0xffU},/**< not used */
        {0xffU,  0xffU},/**< not used */
    },
    {
        {0x02U,  0x00U},/**< matrix led 25 */
        {0x02U,  0x01U},/**< matrix led 26 */
        {0x02U,  0x02U},/**< matrix led 27 */
        {0x02U,  0x03U},/**< matrix led 28 */
        {0x02U,  0x04U},/**< matrix led 29 */
        {0x02U,  0x05U},/**< matrix led 30 */
        {0x02U,  0x06U},/**< matrix led 31 */
        {0x02U,  0x07U},/**< matrix led 32 */
        {0xffU,  0xffU},/**< not used */
        {0xffU,  0xffU},/**< not used */
        {0xffU,  0xffU},/**< not used */
        {0xffU,  0xffU},/**< not used */
    },
};

const __attribute__ ((used,used,section(".parameter_config_53"))) uint8_t g_used_matrix_led_k[USED_MATRIX_CHIP_NUMS][16U] = {
    /**< 0   1   2   3   4   5   6   7   8   9  10  11*/
    {
        100U, /**< matrix led 1  */
        100U, /**< matrix led 2  */
        100U, /**< matrix led 3  */
        100U, /**< matrix led 4  */
        100U, /**< matrix led 5  */
        100U, /**< matrix led 6  */
        100U, /**< matrix led 7  */ 
        100U, /**< matrix led 8  */
        100U, /**< matrix led 9  */
        100U, /**< matrix led 10 */
        100U, /**< matrix led 11 */
        100U, /**< matrix led 12 */
        0xffU, /**< not used */
        0xffU, /**< not used */
        0xffU, /**< not used */
        0xffU, /**< not used */
    },
    {
        100U, /**< matrix led 13  */
        100U, /**< matrix led 14  */
        100U, /**< matrix led 15  */
        100U, /**< matrix led 16  */
        100U, /**< matrix led 17  */
        100U, /**< matrix led 18  */
        100U, /**< matrix led 19  */ 
        100U, /**< matrix led 20  */
        100U, /**< matrix led 21  */
        100U, /**< matrix led 22  */
        100U, /**< matrix led 23  */
        100U, /**< matrix led 24  */
        0xffU, /**< not used */
        0xffU, /**< not used */
        0xffU, /**< not used */
        0xffU, /**< not used */
    },
    {
        100U, /**< matrix led 25  */
        100U, /**< matrix led 26  */
        100U, /**< matrix led 27  */
        100U, /**< matrix led 28  */
        100U, /**< matrix led 29  */
        100U, /**< matrix led 30  */
        100U, /**< matrix led 31  */
        100U, /**< matrix led 32  */
        0xffU, /**< not used */
        0xffU, /**< not used */
        0xffU, /**< not used */
        0xffU, /**< not used */ 
        0xffU, /**< not used */
        0xffU, /**< not used */
        0xffU, /**< not used */
        0xffU, /**< not used */
    }
};
#endif

const __attribute__ ((used,used,section(".parameter_config_62"))) uint8_t u8_lb_hb_welcom_en = @HB_LB_ANIMATION_ENABLE@U;

/** Motor configuration table */
const __attribute__ ((used,used,section(".parameter_config_60"))) MOTOR_CONIFICTION_TABLE_T motor_config_infomation = {
    .motor_properties = {
        @MOTOR_LOW_VOLTAGE@,
        @MOTOR_OVER_VOLTAGE@,
        @MOTOR_DIRECTION@,
        @MOTOR_FULL_STEP_1MM@,     // Full steps per mm, scaled by 100
        @MOTOR_DISTANCE_RATIO_1MM@ // Wall command ratio at 10 m, scaled by 100
    },
    .motor_position_info = {
        /* Position order: POS1, POS2, POS3, POS4, POS5 */
        { @MOTOR_POSITION_POS1_STEP_TO_POS@, @MOTOR_POSITION_POS2_STEP_TO_POS@, @MOTOR_POSITION_POS3_STEP_TO_POS@, @MOTOR_POSITION_POS4_STEP_TO_POS@, @MOTOR_POSITION_POS5_STEP_TO_POS@ }, // Steps to each position from Pos1, FS*100
        { @MOTOR_POSITION_POS1_DISTANCE_TO_POS@, @MOTOR_POSITION_POS2_DISTANCE_TO_POS@, @MOTOR_POSITION_POS3_DISTANCE_TO_POS@, @MOTOR_POSITION_POS4_DISTANCE_TO_POS@, @MOTOR_POSITION_POS5_DISTANCE_TO_POS@ }, // Head spindle distance to Pos1, mm*100
        { @MOTOR_POSITION_POS1_WALL_POS@, @MOTOR_POSITION_POS2_WALL_POS@, @MOTOR_POSITION_POS3_WALL_POS@, @MOTOR_POSITION_POS4_WALL_POS@, @MOTOR_POSITION_POS5_WALL_POS@ }, // Wall position at 10 m, mm
        { @MOTOR_POSITION_POS1_ANGLE@, @MOTOR_POSITION_POS2_ANGLE@, @MOTOR_POSITION_POS3_ANGLE@, @MOTOR_POSITION_POS4_ANGLE@, @MOTOR_POSITION_POS5_ANGLE@ } // Angle to each position, degree*100
    },
    .motor_operation_info = {
        /* running current[mA], holding current[mA], acceleration[VS/s^2], min speed[VS/s], normal speed[VS/s], max speed[VS/s] */
        { @MOTOR_REFERENCE_RUN_RUNNING_CURRENT@, @MOTOR_REFERENCE_RUN_HOLDING_CURRENT@, @MOTOR_REFERENCE_RUN_ACCELERATION@, @MOTOR_REFERENCE_RUN_MIN_SPEED@, @MOTOR_REFERENCE_RUN_NORMAL_SPEED@, @MOTOR_REFERENCE_RUN_MAX_SPEED@ }, // Reference run parameters
        { @MOTOR_NORMAL_RUN_RUNNING_CURRENT@, @MOTOR_NORMAL_RUN_HOLDING_CURRENT@, @MOTOR_NORMAL_RUN_ACCELERATION@, @MOTOR_NORMAL_RUN_MIN_SPEED@, @MOTOR_NORMAL_RUN_NORMAL_SPEED@, @MOTOR_NORMAL_RUN_MAX_SPEED@ }  // Normal run parameters
    },
    .motor_step_mode = @MOTOR_STEP_MODE@, // Microstep mode
    .motor_afs_info = {
        /* C mode, V mode, E mode; angle*100 */
        { @MOTOR_AFS_LEVEL0_C_MODE@, @MOTOR_AFS_LEVEL0_V_MODE@, @MOTOR_AFS_LEVEL0_E_MODE@ }, // LEVEL0
        { @MOTOR_AFS_LEVEL1_C_MODE@, @MOTOR_AFS_LEVEL1_V_MODE@, @MOTOR_AFS_LEVEL1_E_MODE@ }, // LEVEL1
        { @MOTOR_AFS_LEVEL2_C_MODE@, @MOTOR_AFS_LEVEL2_V_MODE@, @MOTOR_AFS_LEVEL2_E_MODE@ }, // LEVEL2
        { @MOTOR_AFS_LEVEL3_C_MODE@, @MOTOR_AFS_LEVEL3_V_MODE@, @MOTOR_AFS_LEVEL3_E_MODE@ }  // LEVEL3
    },
    .dc_motor_level_info = {
        @MOTOR_DC_LEVEL0@, // Level0 voltage, V*100
        @MOTOR_DC_LEVEL1@, // Level1 voltage, V*100
        @MOTOR_DC_LEVEL2@, // Level2 voltage, V*100
        @MOTOR_DC_LEVEL3@  // Level3 voltage, V*100
    },
};

extern const __attribute__ ((section(".parameter_config_63"))) Loudness_Suncoe_EEA5[LOUDNESS_MAX_IDX] = {
    67, 79, 90, 96, 100, 86, 83, 70, 65
};

#endif

#ifndef APP_CONFIG_H
#define APP_CONFIG_H

#include <stdint.h>

#define NULL (void *)0

#define PROJECT_A_SMALL          ( 0U )
#define PROJECT_A_PLUS_PLUS      ( 1U )
#define PROJECT_A_PLUS           ( 2U )
#define PROJECT_MAX              ( 3U )

#define PROJECT_NAME             ( @PROJECT_NAME@ )

#define VERSION_V4               ( 0U )
#define VERSION_V5               ( 1U )

#define EEA_X @EEA_X@

#define SYSTEM_COM_VERION        ( @SYSTEM_COM_VERION@ )

#if ( PROJECT_NAME == PROJECT_A_SMALL || PROJECT_NAME == PROJECT_A_PLUS )
#define USED_MATRIX_FUNCTION     ( 0U )
#else
#define USED_MATRIX_FUNCTION     ( 1U )
#endif

#if ( USED_MATRIX_FUNCTION == 1U )
#define MATRIX_TPS92662A         (0x00U)
#define MATRIX_TPS92663A         (0x01U)
#define MATRIX_TPS92664A         (0x02U)
#define MATRIX_MAX_TYPE          (0x03U)
typedef uint8_t MATRIX_TYPE_T;
#endif

#define CVCC_TPS929120           (0x00U)/**< 12 CHANNELS */
#define CVCC_TPS929160           (0x01U)/**< 16 CHANNELS */
#define CVCC_TPS929240           (0x02U)/**< 24 CHANNELS */
#define CVCC_NSL20912            (0x03U)/**< 12 CHANNELS */

typedef uint8_t CVCC_TYPE_T;

#if ( USED_MATRIX_FUNCTION == 1U )
#define USED_MATRIX_CHIP_NUMS    ( @USED_MATRIX_CHIP_NUMS@U )
#define USED_MATRIX_LED_NUMS     ( @USED_MATRIX_LED_NUMS@U )
#endif
#define USED_CVCC_CHIP_NUMS      ( @USED_CVCC_CHIP_NUMS@U )

#define SUB_UARTCAN_0  ( 0U )
#define SUB_UARTCAN_1  ( 1U )
#define SUB_UARTCAN_2  ( 2U )
typedef uint8_t UARTCAN_IDX_T;

#define ADC_USED_SW    ( 0U )
#define ADC_USED_HW    ( 1U )
#define ADC_TRIG_METHOD  ( ADC_USED_HW )

#define CVCC_OUTPUT_VOLTAGE_LEVELS ( @CVCC_OUTPUT_VOLTAGE_LEVELS@U )

#define DERATE_THEORY_PWM_DERATE     ( 0U )/**< 数字占空比降额 */
#define DERATE_THEORY_CURRENT_DERATE ( 1U )/**< 电流值降额 */
#define LBHB_DERATE_THEORY   ( DERATE_THEORY_CURRENT_DERATE )
#define SIGNAL_DERATE_THEORY ( DERATE_THEORY_PWM_DERATE )

#if ( USED_MATRIX_FUNCTION == 1U )
#define HB_WITH_ADB   ( 1U )/**< HB作为ADB输出 */
#else
#define HB_WITH_ADB   ( 0U )/**< HB没有ADB输出 */
#endif

#if ( PROJECT_NAME == PROJECT_A_SMALL )
#define HB_CH_NUM     ( 1U )
#else
#define HB_CH_NUM     ( 3U )
#endif

#define SIGNAL_LED_CURRENT_METHOD    ( @SIGNAL_LED_CURRENT_METHOD@U )/**< 0: 电流设定+PWM调光方式 1: 恒流芯片方式,电流不变，改占空比 */
#define TI_DRL_CURRENT_DERATE_METHOD ( @TI_DRL_CURRENT_DERATE_METHOD@U )/**< 0: TI_DRL使用数字降额 1: TI_DRL使用电流降额，PL用数字降额 */

#if ( USED_MATRIX_FUNCTION == 1U )
typedef struct
{
    uint8_t ic_addr;            /**< 矩阵芯片地址 */
    MATRIX_TYPE_T ic_type;      /**< 矩阵芯片类型 */
    UARTCAN_IDX_T ic_uartchn;   /**< 矩阵芯片通讯通道 */
    uint8_t ic_io_sw_nums;      /**< 矩阵芯片开关个数 */
    uint16_t ic_sw_mask;        /**< 矩阵芯片开关掩码 */
}APP_Matrix_Cfg_T;

typedef struct
{
    uint8_t matrix_id;
    uint8_t sw_id;
}APP_ADB_LED_POS_Cfg_T;

#endif

typedef struct
{
    uint8_t ic_addr;            /**< CVCC芯片地址 */
    CVCC_TYPE_T ic_type;        /**< CVCC芯片类型 */
    UARTCAN_IDX_T ic_uartchn;   /**< CVCC芯片通讯通道 */
    uint8_t ic_io_sw_nums;      /**< CVCC芯片开关个数 */
    uint32_t ic_sw_mask;        /**< CVCC芯片开关掩码 */
    uint8_t ic_max_current;     /**< CVCC芯片最大可设电流值 */
}APP_Cvcc_Cfg_T;

/**< Config 1 流水点亮灯珠分配，当前为40颗灯珠 */
#define TI_USED_LED_NUMS           (  @TI_USED_LED_NUMS@U )
#define TI_USED_LED_NUMS_DATA_LENS (   @TI_USED_LED_NUMS_DATA_LENS@U ) /**< 需要2*32bit的数据才能表示64颗灯珠的状态：2 = 64 / 32 */
#define TI_SWEEP_CYCLE_TIME        ( @TI_SWEEP_CYCLE_TIME@U ) /**< 每步流水持续时间，单位：ms */
#define TI_SWEEP_USER_STEP         (  @TI_SWEEP_USER_STEP@U ) /**< 用户设置的流水步数，最大不能超过20步 */
#define TI_SWEEP_STEP_MAX          (  @TI_SWEEP_STEP_MAX@U ) /**< 最大流水步数 */

#define TI_SEEP_ANIMATION_MODE     ( @TI_SEEP_ANIMATION_MODE@U )  /**< 0:流水动画1 1:流水动画2 */
/** MOTOR CONFIGURATION */
#define MOTOR_PUSH  ( 0u ) /**< Positive direction. */
#define MOTOR_PULL   ( 1u ) /**< N direction */
#define MOTOR_DIRECT_MAX ( 2u )
typedef uint32_t MOTOR_RIRECTION_TYPE;

#define MOTOR_POS_MECHANICAL_BLOCK_DOWNWARD ( 0u ) /**< POS1 */
#define MOTOR_POS_CAN_BLOCK_DOWNWARD ( 1u ) /**< POS2 */
#define MOTOR_POS_SAFETY_POSITION ( 2u ) /**< POS3 */
#define MOTOR_POS_ZERO_POSITION ( 3u ) /**< POS4 */
#define MOTOR_POS_CAN_BLOCK_UPWARD ( 4u ) /**< POS5 */
#define MOTOR_POS_MECHANICAL_BLOCK_UPWARD ( 5u ) /**< POS6 */
#define MOTOR_POS_REFERENCE_POSITION ( 6u ) /**< POS7 */
#define MOTOR_POS_MAX ( 5u )
typedef uint8_t MOTOR_POS_TYPE;

#define MOTOR_MODE_NORMAOL ( 0u )
#define MOTOR_MODE_COLD    ( 1u )
#define MOTOR_MODE_MAX     ( 2u )
typedef uint8_t MOTOR_MODE_TYPE;

#define MOTOR_STEP_MODE_1_8_STEP  ( 5u )
#define MOTOR_STEP_MODE_1_16_STEP ( 6u )
#define MOTOR_STEP_MODE_1_32_STEP  ( 7u )

typedef uint8_t MOTOR_STEP_MODE_TYPE;

typedef struct
{
   uint8_t motor_lowvoltage;/* v *10*/
   uint8_t motor_overvoltage;/* v *10*/
   MOTOR_RIRECTION_TYPE motor_director; /**< PUSH OR POP */
   uint16_t motor_full_step_1mm; /**< real*100 of the real FS/mm */
   uint16_t motor_distance_ratio_1mm; /**< real*100 Distance ratio */
}MOTOR_GENERAL_PROTERY_T;

typedef struct
{
   uint16_t step_to_pos[MOTOR_POS_MAX]; /**< FS*100 */
   uint16_t head_spindle_distance_to_pos[MOTOR_POS_MAX]; /**< mm*100 */
   int16_t pos_on_wall[MOTOR_POS_MAX];
   int16_t angle_to_pos[MOTOR_POS_MAX]; /**< degrees*100 */
}MOTOR_POSITION_INFO_T;

typedef struct
{
   uint16_t running_current; /**< mA */
   uint16_t holding_current; /**< mA */
   uint16_t acceleration; /**< VS/s^2 */
   uint16_t min_start_up_speed; /**< VS/s */
   uint16_t normal_movement_speed;
   uint16_t max_movement_speed; /**< VS/s */
}MOTOR_RUN_INFO_T;

typedef struct
{
   MOTOR_RUN_INFO_T reference_run;
   MOTOR_RUN_INFO_T normol_operate;
}MOTOR_OPERATE_INFO_T;

/** Motor configuration table */
typedef struct
{
   MOTOR_GENERAL_PROTERY_T motor_properties;
   MOTOR_POSITION_INFO_T motor_position_info;
   MOTOR_OPERATE_INFO_T motor_operation_info;
   MOTOR_STEP_MODE_TYPE motor_step_mode;
   int16_t motor_afs_info[4][3];
   uint16_t dc_motor_level_info[4];
}MOTOR_CONIFICTION_TABLE_T;

@LOCK_UNLOCK_MACROS@

@CHANNEL_LED_COUNT_MACROS@

@PARAMETER_CONFIG_EXTERN_DECLARATIONS@

typedef struct
{
    uint16_t config_word0;
    uint16_t config_word1;
    uint16_t config_word2;
}CHCM_Cfg_T;

@CHCM_CFG_INDEX_DEFINITIONS@

@LOUDNESS_INDEX_DEFINITIONS@

@CHCM_AND_MATRIX_EXTERN_DECLARATIONS@

#endif

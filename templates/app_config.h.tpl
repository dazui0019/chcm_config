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

#define EEA_X VERSION_V5

#define SYSTEM_COM_VERION        ( VERSION_V5 )

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
#define USED_MATRIX_CHIP_NUMS    ( 3U )
#define USED_MATRIX_LED_NUMS     ( 32U )
#endif
#define USED_CVCC_CHIP_NUMS      (11U )

#define SUB_UARTCAN_0  ( 0U )
#define SUB_UARTCAN_1  ( 1U )
#define SUB_UARTCAN_2  ( 2U )
typedef uint8_t UARTCAN_IDX_T;

#define ADC_USED_SW    ( 0U )
#define ADC_USED_HW    ( 1U )
#define ADC_TRIG_METHOD  ( ADC_USED_HW )

#define CVCC_OUTPUT_VOLTAGE_LEVELS ( 18U )

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

#define SIGNAL_LED_CURRENT_METHOD    ( 1U )/**< 0: 电流设定+PWM调光方式 1: 恒流芯片方式,电流不变，改占空比 */
#define TI_DRL_CURRENT_DERATE_METHOD ( 0U )/**< 0: TI_DRL使用数字降额 1: TI_DRL使用电流降额，PL用数字降额 */

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
#define TI_USED_LED_NUMS           (  40U )
#define TI_USED_LED_NUMS_DATA_LENS (   2U ) /**< 需要2*32bit的数据才能表示64颗灯珠的状态：2 = 64 / 32 */
#define TI_SWEEP_CYCLE_TIME        ( 200U ) /**< 每步流水持续时间，单位：ms */
#define TI_SWEEP_USER_STEP         (  20U ) /**< 用户设置的流水步数，最大不能超过20步 */
#define TI_SWEEP_STEP_MAX          (  20U ) /**< 最大流水步数 */

#define TI_SEEP_ANIMATION_MODE     ( 2U )  /**< 0:流水动画1 1:流水动画2 */
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
   int16_t  angle_to_pos[MOTOR_POS_MAX]; /**< degrees*100 */
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
/* Const memory section */
extern const __attribute__ ((section(".parameter_config_0"))) uint8_t g_communication_version;
extern const __attribute__ ((section(".parameter_config_1"))) uint8_t g_used_cvcc_ic_nums;
extern const __attribute__ ((section(".parameter_config_2"))) APP_Cvcc_Cfg_T App_cvcc_cfg_L[USED_CVCC_CHIP_NUMS];
extern const __attribute__ ((section(".parameter_config_3"))) uint8_t g_cvcc_out_voltage_table[CVCC_OUTPUT_VOLTAGE_LEVELS];
extern const __attribute__ ((section(".parameter_config_60"))) MOTOR_CONIFICTION_TABLE_T motor_config_infomation;

/* Declaration for custom storage class: Const */
/* extern const __attribute__ ((section(".parameter_config_4"))) uint32_t u32_ti_sweep_frame[TI_SWEEP_USER_STEP + 1u][TI_USED_LED_NUMS_DATA_LENS];*/

extern const __attribute__ ((section(".parameter_config_4"))) uint8_t u8_ti_sweep_led_nums;/**< Number of used LEDs */
extern const __attribute__ ((section(".parameter_config_5"))) uint8_t u8_ti_sweep_led_k[TI_SWEEP_USER_STEP + 1u][TI_USED_LED_NUMS];/* Referenced by:
                                                 * '<S18>/cvcc_current_duty_mode_assigment'
                                                 * '<S91>/assign_cvcc_duty_mode_chart'
                                                 */

/**< lock/unlock animation control define */
#define LOCK_ANIMATION_MODE1    (  1U )  /**< 闭锁模式1 */
#define LOCK_ANIMATION_MODE2    (  2U )  /**< 闭锁模式2 */
#define LOCK_ANIMATION_MODE3    (  3U )  /**< 闭锁模式3 */
#define LOCK_ANIMATION_MODE4    (  4U )  /**< 闭锁模式4 */
#define LOCK_ANIMATION_MODE5    (  5U )  /**< 闭锁模式5 */
#define UNLOCK_ANIMATION_MODE1  (  6U )  /**< 解锁模式1 */
#define UNLOCK_ANIMATION_MODE2  (  7U )  /**< 解锁模式2 */
#define UNLOCK_ANIMATION_MODE3  (  8U )  /**< 解锁模式3 */
#define UNLOCK_ANIMATION_MODE4  (  9U )  /**< 解锁模式4 */
#define UNLOCK_ANIMATION_MODE5  ( 10U )  /**< 解锁模式5 */

/**< lock/unlock animation mode total frames */
#define LOCK_MODE1_TOTAL_STEP    ( 301U )  /**< 闭锁模式1总步数 */
#define LOCK_MODE2_TOTAL_STEP    ( 0U )  /**< 闭锁模式2总步数 */
#define LOCK_MODE3_TOTAL_STEP    ( 0U )  /**< 闭锁模式3总步数 */
#define LOCK_MODE4_TOTAL_STEP    ( 0U )  /**< 闭锁模式4总步数 */
#define LOCK_MODE5_TOTAL_STEP    ( 0U )  /**< 闭锁模式5总步数 */
#define UNLOCK_MODE1_TOTAL_STEP  ( 301U )  /**< 解锁模式1总步数 */
#define UNLOCK_MODE2_TOTAL_STEP  ( 0U )  /**< 解锁模式2总步数 */
#define UNLOCK_MODE3_TOTAL_STEP  ( 0U )  /**< 解锁模式3总步数 */
#define UNLOCK_MODE4_TOTAL_STEP  ( 0U )  /**< 解锁模式4总步数 */
#define UNLOCK_MODE5_TOTAL_STEP  ( 0U )  /**< 解锁模式5总步数 */

#define LOCK_UNLOCK_MAX_MODE_NUMS  ( 10U ) /**< 最大闭锁/解锁动画模式数 */

#define TI_DRL_PL_LED_NUMS         ( 64U ) /**< TI/DRL/PL使用的灯珠数 */
#define TI_LED_NUMS                ( 0U  ) /**< TI 使用的灯珠数 */
#define DRL_PL_0_LED_NUMS          ( 0U  ) /**< DRL/PL0 使用的灯珠数 */
#define DRL_0_LED_NUMS             ( 0U  ) /**< DRL0 使用的灯珠数 */
#define DRL_PL_1_LED_NUMS          ( 0U  ) /**< DRL/PL1 使用的灯珠数 */
#define DRL_1_LED_NUMS             ( 0U  ) /**< DRL1 使用的灯珠数 */
#define DRL_PL_2_LED_NUMS          ( 0U  ) /**< DRL/PL2 使用的灯珠数 */
#define DRL_2_LED_NUMS             ( 0U  ) /**< DRL2 使用的灯珠数 */
#define PL_LED_NUMS                ( 0U  ) /**< PL 使用的灯珠数 */

#define SIGNAL_ANIMATION_LED_NUMS  ( 54U ) /**< 信号动画使用的灯珠数 */

extern const __attribute__ ((section(".parameter_config_6"))) uint16_t u8_lock_unlock_animation_total_steps[LOCK_UNLOCK_MAX_MODE_NUMS];
extern const __attribute__ ((section(".parameter_config_7"))) uint8_t u8_lock_mode_type_nums;
/* extern const __attribute__ ((section(".parameter_config_9"))) uint16_t u16_lock_mode_address[5u]; */
extern const __attribute__ ((section(".parameter_config_8"))) uint8_t u8_unlock_mode_type_nums;
/* extern const __attribute__ ((section(".parameter_config_11"))) uint16_t u16_unlock_mode_address[5u]; */

extern const __attribute__ ((section(".parameter_config_9"))) uint8_t u8_lock_mode1_animation[LOCK_MODE1_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS];
extern const __attribute__ ((section(".parameter_config_10"))) uint8_t u8_lock_mode2_animation[LOCK_MODE2_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS];
extern const __attribute__ ((section(".parameter_config_11"))) uint8_t u8_lock_mode3_animation[LOCK_MODE3_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS];
extern const __attribute__ ((section(".parameter_config_12")))  uint8_t u8_lock_mode4_animation[LOCK_MODE4_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS];
extern const __attribute__ ((section(".parameter_config_13")))  uint8_t u8_lock_mode5_animation[LOCK_MODE5_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS];
extern const __attribute__ ((section(".parameter_config_14")))  uint8_t u8_unlock_mode1_animation[UNLOCK_MODE1_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS];
extern const __attribute__ ((section(".parameter_config_15")))  uint8_t u8_unlock_mode2_animation[UNLOCK_MODE2_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS];
extern const __attribute__ ((section(".parameter_config_16")))  uint8_t u8_unlock_mode3_animation[UNLOCK_MODE3_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS];
extern const __attribute__ ((section(".parameter_config_17")))  uint8_t u8_unlock_mode4_animation[UNLOCK_MODE4_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS];
extern const __attribute__ ((section(".parameter_config_18")))  uint8_t u8_unlock_mode5_animation[UNLOCK_MODE5_TOTAL_STEP][SIGNAL_ANIMATION_LED_NUMS];

/* extern const __attribute__ ((section(".parameter_config_22"))) uint8_t *signal_animation_data[LOCK_UNLOCK_MAX_MODE_NUMS]; */
/* Exported data declaration */

/* Const memory section */
/* Declaration for custom storage class: Const */
extern const __attribute__ ((section(".parameter_config_19"))) uint8_t u8_cvcc_k_array[12][24];/* Referenced by:
                                              * '<S19>/cvcc_current_duty_mode_assigment'
                                              * '<S93>/cvcc_current_init_proc'
                                              */
/* 各恒流芯片每个通道输出电流值K系数 */
extern const __attribute__ ((section(".parameter_config_20"))) uint8_t u8_drl_0_cvcc_map_array[2][2];/* Referenced by:
                                                    * '<S19>/drl_0_map_array'
                                                    * '<S92>/drl_0_map_array'
                                                    * '<S93>/drl_0_map_array'
                                                    */
/* 恒流类型4输出通道
   与TI互斥关闭，单独的DRL通道 */
extern const __attribute__ ((section(".parameter_config_21"))) uint8_t u8_drl_0_cvcc_map_nums;/* Referenced by:
                                             * '<S19>/drl_0_map_nums'
                                             * '<S92>/drl_0_map_nums'
                                             * '<S93>/drl_0_map_nums'
                                             */
extern const __attribute__ ((section(".parameter_config_22")))  uint8_t u8_drl_0_unlock_lock_offset;

/* 恒流类型4输出通道个数 */
extern const __attribute__ ((section(".parameter_config_23"))) uint8_t u8_drl_1_cvcc_map_array[2][2];/* Referenced by:
                                                    * '<S19>/drl_1_map_array'
                                                    * '<S92>/drl_1_map_array'
                                                    * '<S93>/drl_1_map_array'
                                                    */
/* 恒流类型6输出通道
   与TI互斥降额，单独的DRL通道 */
extern const __attribute__ ((section(".parameter_config_24"))) uint8_t u8_drl_1_cvcc_map_nums;/* Referenced by:
                                             * '<S19>/drl_1_map_nums'
                                             * '<S92>/drl_1_map_nums'
                                             * '<S93>/drl_1_map_nums'
                                             */
extern const __attribute__ ((section(".parameter_config_25")))  uint8_t u8_drl_1_unlock_lock_offset;

/* 恒流类型6输出通道个数 */
extern const __attribute__ ((section(".parameter_config_26"))) uint8_t u8_drl_2_cvcc_map_array[2][2];/* Referenced by:
                                                    * '<S19>/drl_2_map_array'
                                                    * '<S92>/drl_2_map_array'
                                                    * '<S93>/drl_2_map_array'
                                                    */
/* 恒流类型8输出通道
   单独的DRL通道 */
extern const __attribute__ ((section(".parameter_config_27"))) uint8_t u8_drl_2_cvcc_map_nums;/* Referenced by:
                                             * '<S19>/drl_2_map_nums'
                                             * '<S92>/drl_2_map_nums'
                                             * '<S93>/drl_2_map_nums'
                                             */
extern const __attribute__ ((section(".parameter_config_28")))  uint8_t u8_drl_2_unlock_lock_offset;

/* 恒流类型8输出通道个数 T2 */
extern const __attribute__ ((section(".parameter_config_29"))) uint8_t u8_drl_pl_0_cvcc_map_array[20][2];/* Referenced by:
                                                       * '<S19>/drl_pl_0_map_array'
                                                       * '<S92>/drl_pl_0_map_array'
                                                       * '<S93>/drl_pl_0_map_array'
                                                       */
/* 恒流类型3输出通道
   与TI互斥关闭，DRL和PL共用通道 */
extern const __attribute__ ((section(".parameter_config_30"))) uint8_t u8_drl_pl_0_cvcc_map_nums;/* Referenced by:
                                                * '<S19>/drl_pl_0_map_nums'
                                                * '<S92>/drl_pl_0_map_nums'
                                                * '<S93>/drl_pl_0_map_nums'
                                                */
extern const __attribute__ ((section(".parameter_config_31")))  uint8_t u8_drl_pl_0_pl_duty;
extern const __attribute__ ((section(".parameter_config_32")))  uint8_t u8_drl_pl_0_unlock_lock_offset;

/* 恒流类型3输出通道个数 T3 */
extern const __attribute__ ((section(".parameter_config_33"))) uint8_t u8_drl_pl_1_cvcc_map_array[16][2];/* Referenced by:
                                                       * '<S19>/drl_pl_1_map_array'
                                                       * '<S92>/drl_pl_1_map_array'
                                                       * '<S93>/drl_pl_1_map_array'
                                                       */
/* 恒流类型5输出通道
   与TI互斥降额，DRL和PL共用通道。 */
extern const __attribute__ ((section(".parameter_config_34"))) uint8_t u8_drl_pl_1_cvcc_map_nums;/* Referenced by:
                                                * '<S19>/drl_pl_1_map_nums'
                                                * '<S92>/drl_pl_1_map_nums'
                                                * '<S93>/drl_pl_1_map_nums'
                                                */
extern const __attribute__ ((section(".parameter_config_35")))  uint8_t u8_drl_pl_1_pl_duty;
extern const __attribute__ ((section(".parameter_config_36")))  uint8_t u8_drl_pl_1_unlock_lock_offset;
/* 恒流类型5输出通道个数 */
extern const __attribute__ ((section(".parameter_config_37"))) uint8_t u8_drl_pl_2_cvcc_map_array[2][2];/* Referenced by:
                                                       * '<S19>/drl_pl_2_map_array'
                                                       * '<S92>/drl_pl_2_map_array'
                                                       * '<S93>/drl_pl_2_map_array'
                                                       */
/* 恒流类型7输出通道
   单独的DRL和PL共用通道 */
extern const __attribute__ ((section(".parameter_config_38"))) uint8_t u8_drl_pl_2_cvcc_map_nums;/* Referenced by:
                                                * '<S19>/drl_pl_2_map_nums'
                                                * '<S92>/drl_pl_2_map_nums'
                                                * '<S93>/drl_pl_2_map_nums'
                                                */
extern const __attribute__ ((section(".parameter_config_39")))  uint8_t u8_drl_pl_2_pl_duty;
extern const __attribute__ ((section(".parameter_config_40")))  uint8_t u8_drl_pl_2_unlock_lock_offset;
/* 恒流类型7输出通道个数 */
extern const __attribute__ ((section(".parameter_config_41"))) uint8_t u8_hb_adb_mode;  /* Referenced by: '<S5>/u8_hb_adb_mode' */
/* 配置当前HB是否为ADB模式 */
extern const __attribute__ ((section(".parameter_config_42"))) uint8_t u8_pl_0_cvcc_map_array[2][2];/* Referenced by:
                                                   * '<S19>/pl_0_map_array'
                                                   * '<S92>/pl_0_map_array'
                                                   * '<S93>/pl_0_map_array'
                                                   */
/* 恒流类型9输出通道
   单独的PL通道 */
extern const __attribute__ ((section(".parameter_config_43"))) uint8_t u8_pl_0_cvcc_map_nums;/* Referenced by:
                                            * '<S19>/pl_0_map_nums'
                                            * '<S92>/pl_0_map_nums'
                                            * '<S93>/pl_0_map_nums'
                                            */
extern const __attribute__ ((section(".parameter_config_44")))  uint8_t u8_pl_0_unlock_lock_offset;

/* 恒流类型9输出通道个数 T8 */
extern const __attribute__ ((section(".parameter_config_45"))) uint8_t u8_pl_cvcc_map_array[18][2];/* Referenced by:
                                                 * '<S19>/pl_map_array'
                                                 * '<S92>/pl_map_array'
                                                 * '<S93>/pl_map_array'
                                                 */
/* 恒流类型9输出通道
   单独的PL通道 */
extern const __attribute__ ((section(".parameter_config_46"))) uint8_t u8_pl_cvcc_map_nums;/* Referenced by:
                                          * '<S19>/pl_map_nums'
                                          * '<S92>/pl_map_nums'
                                          * '<S93>/pl_map_nums'
                                          */
extern const __attribute__ ((section(".parameter_config_47")))  uint8_t u8_pl_cvcc_current;
extern const __attribute__ ((section(".parameter_config_48")))  uint8_t u8_pl_unlock_lock_offset;
/* 恒流类型9输出通道个数 */
extern const __attribute__ ((section(".parameter_config_49"))) uint8_t u8_pl_duty_cfg;   /* Referenced by: '<S1>/pl_duty_cfg' */
extern const __attribute__ ((section(".parameter_config_50"))) uint8_t u8_ti_cvcc_map_array[40][2];/* Referenced by:
                                                 * '<S19>/ti_channel'
                                                 * '<S92>/ti_channel'
                                                 * '<S93>/ti_channel'
                                                 */
/* 恒流类型1输出通道
   单独的TI通道输出 T1 */
extern const __attribute__ ((section(".parameter_config_51"))) uint8_t u8_ti_cvcc_map_nums;/* Referenced by:
                                          * '<S19>/ti_nums'
                                          * '<S92>/ti_nums'
                                          * '<S93>/ti_nums'
                                          */
/* 恒流类型1输出通道个数 */
extern const __attribute__ ((section(".parameter_config_52"))) uint8_t u8_ti_drl_pl_cvcc_map_array[2][2];/* Referenced by:
                                                         * '<S19>/ti_drl_pl_channel'
                                                         * '<S92>/ti_drl_pl_channel'
                                                         * '<S923>/ti_drl_pl_channel'
                                                         */
/* 恒流类型2输出通道
   TI/DRL/PL共用通道 */
extern const __attribute__ ((section(".parameter_config_53"))) uint8_t u8_ti_drl_pl_cvcc_map_nums;/* Referenced by:
                                      4           * '<S19>/ti_drl_pl_nums'
                                                 * '<S92>/ti_drl_pl_nums'
                                                 * '<S93>/ti_drl_pl_nums'
                                                 */
extern const __attribute__ ((section(".parameter_config_54")))  uint8_t u8_ti_drl_pl_unlock_lock_offset;

extern const __attribute__ ((section(".parameter_config_55")))  uint8_t u8_adas_cvcc_map_array[16][2];

extern const __attribute__ ((section(".parameter_config_56")))  uint8_t u8_adas_cvcc_map_nums;
extern const __attribute__ ((section(".parameter_config_57")))  uint8_t u8_adas_cvcc_current;

/* 恒流类型2输出通道个数 */
/* Declaration for custom storage class: Const */
extern const __attribute__ ((section(".parameter_config_58"))) uint8_t u8_ti_drl_current_method;
                            /* Referenced by: '<S1>/u8_ti_drl_current_method' */

/* 信号灯电流输出方式：
   1. 实时更新电流值（0）。
   2. 只上电更新一次电流，基础电流固定设置为ti或者drl。 */

/* Const memory section */
/* Declaration for custom storage class: Const */
extern const __attribute__ ((section(".parameter_config_59"))) uint8_t u8_drl_ntc_default_derate;/* Referenced by: '<S4>/Constant2' */

typedef struct 
{
    uint16_t config_word0;
    uint16_t config_word1;
    uint16_t config_word2;
}CHCM_Cfg_T;

#define CHCM_CFG_IDX_0_INACTIVE                ( @CHCM_CFG_IDX_0_INACTIVE@U )
#define CHCM_CFG_IDX_1_SIGNAL_LED_CURRENT      ( @CHCM_CFG_IDX_1_SIGNAL_LED_CURRENT@U )
#define CHCM_CFG_IDX_2_LSD_OUT1                ( @CHCM_CFG_IDX_2_LSD_OUT1@U )
#define CHCM_CFG_IDX_3_LSD_OUT2                ( @CHCM_CFG_IDX_3_LSD_OUT2@U )
#define CHCM_CFG_IDX_4_HSD_OUT1                ( @CHCM_CFG_IDX_4_HSD_OUT1@U )
#define CHCM_CFG_IDX_5_HSD_OUT2                ( @CHCM_CFG_IDX_5_HSD_OUT2@U )
#define CHCM_CFG_IDX_6_HSD_OUT3                ( @CHCM_CFG_IDX_6_HSD_OUT3@U )
#define CHCM_CFG_IDX_7_HSD_OUT4                ( @CHCM_CFG_IDX_7_HSD_OUT4@U )    /**< only used in A++ project */
#define CHCM_CFG_IDX_8_LSD_IN1                 ( @CHCM_CFG_IDX_8_LSD_IN1@U )     /**< only used in A++ project */
#define CHCM_CFG_IDX_9_LSD_IN2                 ( @CHCM_CFG_IDX_9_LSD_IN2@U )
#define CHCM_CFG_IDX_10_BUCK_CV                ( @CHCM_CFG_IDX_10_BUCK_CV@U )
#define CHCM_CFG_IDX_11_PL_DUTY                ( @CHCM_CFG_IDX_11_PL_DUTY@U )
#define CHCM_CFG_IDX_12_DRL_NTC_DERATE         ( @CHCM_CFG_IDX_12_DRL_NTC_DERATE@U )
#define CHCM_CFG_IDX_13_LB_NTC_DERATE          ( @CHCM_CFG_IDX_13_LB_NTC_DERATE@U )
#define CHCM_CFG_IDX_14_HB_NTC_DERATE          ( @CHCM_CFG_IDX_14_HB_NTC_DERATE@U )
#define CHCM_CFG_IDX_15_PL_DELAY               ( @CHCM_CFG_IDX_15_PL_DELAY@U )   /**< not used */
#define CHCM_CFG_IDX_16_AFS_TYPE               ( @CHCM_CFG_IDX_16_AFS_TYPE@U )
#define CHCM_CFG_IDX_17_DC_MOTOR_LEVEL         ( @CHCM_CFG_IDX_17_DC_MOTOR_LEVEL@U )
#define CHCM_CFG_IDX_18_STEP_MOTOR_INIT_DIR    ( @CHCM_CFG_IDX_18_STEP_MOTOR_INIT_DIR@U )
#define CHCM_CFG_IDX_19_STEP_MOTOR_BLOCK_STEPS ( @CHCM_CFG_IDX_19_STEP_MOTOR_BLOCK_STEPS@U )
#define CHCM_CFG_IDX_20_RESERVED_20            ( @CHCM_CFG_IDX_20_RESERVED_20@U ) 
#define CHCM_CFG_IDX_21_RESERVED_21            ( @CHCM_CFG_IDX_21_RESERVED_21@U )
#define CHCM_CFG_IDX_22_RESERVED_22            ( @CHCM_CFG_IDX_22_RESERVED_22@U )
#define CHCM_CFG_IDX_23_RESERVED_23            ( @CHCM_CFG_IDX_23_RESERVED_23@U )
#define CHCM_CFG_IDX_24_RESERVED_24            ( @CHCM_CFG_IDX_24_RESERVED_24@U )
#define CHCM_CFG_IDX_25_RESERVED_25            ( @CHCM_CFG_IDX_25_RESERVED_25@U )
#define CHCM_CFG_IDX_26_RESERVED_26            ( @CHCM_CFG_IDX_26_RESERVED_26@U )
#define CHCM_CFG_IDX_MAX                       ( @CHCM_CFG_IDX_MAX@U )

#if EEA_X == VERSION_V5
   #define LOUDNESS_55HZ_IDX   ( 0U )
   #define LOUDNESS_123HZ_IDX  ( 1U )
   #define LOUDNESS_262HZ_IDX  ( 2U )
   #define LOUDNESS_440HZ_IDX  ( 3U )
   #define LOUDNESS_587HZ_IDX  ( 4U )
   #define LOUDNESS_793HZ_IDX  ( 5U )
   #define LOUDNESS_1318HZ_IDX ( 6U )
   #define LOUDNESS_2794HZ_IDX ( 7U )
   #define LOUDNESS_6272HZ_IDX ( 8U )
   #define LOUDNESS_MAX_IDX ( 9U )
#else
   #define LOUDNESS_120HZ_IDX  ( 0U )
   #define LOUDNESS_250HZ_IDX  ( 1U )
   #define LOUDNESS_500HZ_IDX  ( 2U )
   #define LOUDNESS_1000HZ_IDX ( 3U )
   #define LOUDNESS_1500HZ_IDX ( 4U )
   #define LOUDNESS_2000HZ_IDX ( 5U )
   #define LOUDNESS_6000HZ_IDX ( 6U )
   #define LOUDNESS_MAX_IDX ( 7U )
#endif

#if 1
extern const __attribute__ ((section(".parameter_config_61")))  CHCM_Cfg_T CHCM_Cfg[CHCM_CFG_IDX_MAX];
#endif
extern const __attribute__ ((section(".parameter_config_63"))) Loudness_Suncoe_EEA5[LOUDNESS_MAX_IDX];
#if ( USED_MATRIX_FUNCTION == 1U )
extern const __attribute__ ((section(".parameter_config_49"))) uint8_t g_used_matrix_ic_nums;
extern const __attribute__ ((section(".parameter_config_50"))) APP_Matrix_Cfg_T App_matrix_cfg_L[USED_MATRIX_CHIP_NUMS];
extern const __attribute__ ((section(".parameter_config_51"))) uint8_t g_used_matrix_led_nums;
extern const __attribute__ ((section(".parameter_config_52"))) APP_ADB_LED_POS_Cfg_T g_used_matrix_led_id[USED_MATRIX_CHIP_NUMS][16U];
extern const __attribute__ ((section(".parameter_config_53"))) uint8_t g_used_matrix_led_k[USED_MATRIX_CHIP_NUMS][16U];
#endif

extern const __attribute__ ((section(".parameter_config_62"))) uint8_t u8_lb_hb_welcom_en;

#endif

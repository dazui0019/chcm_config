#include "app_config.h"

@BASE_PARAMETER_CONFIG_DEFINITIONS@

/**< Config 0 TI 流水动画控制表格 */
#if 0
@TI_SWEEP_FRAME_DEFINITION@
#endif

/**< TI 流水动画每步每个led灯珠占空比(基于TI原始占空比) */
#if (TI_SEEP_ANIMATION_MODE == 0U)
@TI_SWEEP_LED_K_MODE_0_DEFINITION@
#elif (TI_SEEP_ANIMATION_MODE == 1U)
@TI_SWEEP_LED_K_MODE_1_DEFINITION@
#elif (TI_SEEP_ANIMATION_MODE == 2U)
@TI_SWEEP_LED_K_MODE_2_DEFINITION@
#endif

/**< Config 1 Signale LED 解闭锁动画控制表格 */
@LOCK_UNLOCK_ANIMATION_DEFINITIONS@

/* HB作为矩阵输出，HB的通道3(buck2ch2)绑定的矩阵芯片各个switch的基础占空比值 */
@CVCC_AND_CHANNEL_MAP_DEFINITIONS@

#if 1
@CHCM_CFG_DEFINITION@
#endif

#if ( USED_MATRIX_FUNCTION == 1U )
@MATRIX_DEFINITIONS@
#endif

@WELCOME_DEFINITION@

/**
 * ************************************************************************************
 *                            Motor Configuration Table                               *
 *                                                                                    *
 * ************************************************************************************
 * */
@MOTOR_CONFIG_DEFINITION@

@LOUDNESS_DEFINITION@

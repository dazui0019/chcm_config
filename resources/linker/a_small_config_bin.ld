/*==================================================================================================
*   Project              : RTD AUTOSAR 4.7
*   Platform             : CORTEXM
*   Peripheral           : 
*   Dependencies         : none
*
*   Autosar Version      : 4.7.0
*   Autosar Revision     : ASR_REL_4_7_REV_0000
*   Autosar Conf.Variant :
*   SW Version           : 2.0.0
*   Build Version        : S32K1_RTD_2_0_0_D2308_ASR_REL_4_7_REV_0000_20230804
*
*   (c) Copyright 2020-2023 NXP Semiconductors
*   All Rights Reserved.
*
*   NXP Confidential. This software is owned or controlled by NXP and may only be
*   used strictly in accordance with the applicable license terms. By expressly
*   accepting such terms or by downloading, installing, activating and/or otherwise
*   using the software, you are agreeing that you have read, and that you agree to
*   comply with and are bound by, such license terms. If you do not agree to be
*   bound by the applicable license terms, then you may not retain, install,
*   activate or otherwise use the software.
==================================================================================================*/
/*
* GCC Linker Command File: This linker is demo and  is not part of the production code deliverables.
* 0x00000000    0x0007FFFF  512KB   Flash
* 0x1FFF8000    0x1FFFFFFF  32768  SRAM_L
* 0x20000000    0x20006FFF  28672  SRAM_U
*/

__HARDWRAE_INFO_ADDRESS = 68K;
__HARDWRAE_INFO_LENGTH = 4K;

__APP_HAEADER_ADDRESS = 72K;
__APP_HAEADER_LENGTH = 1K;

__APP_ADDRESS = 73K;
__APP_LENGTH = 407K;

__CONFIG_HEADER_ADDRESS = 480k;
__CONFIG_HEADER_LENGTH = 1K;

__CONFIG_ADDRESS = 481K;
__CONFIG_LENGTH = 31K;

MEMORY
{
    FLASH_HARDWARE_INFO (rx)  : ORIGIN = __HARDWRAE_INFO_ADDRESS, LENGTH = __HARDWRAE_INFO_LENGTH
    FLASH_APP_HAEDER (rx)     : ORIGIN = __APP_HAEADER_ADDRESS,   LENGTH = __APP_HAEADER_LENGTH
    int_flash_interrupts    : ORIGIN = 0x00000000 + __APP_ADDRESS, LENGTH = 0x00000400    /* 1K */    /* Do not change this section */
    int_flash_config        : ORIGIN = 0x00000400 + __APP_ADDRESS, LENGTH = 0x00000010    /* 16bytes */ /* Do not change this section */
    int_flash               : ORIGIN = 0x00000410 + __APP_ADDRESS, LENGTH = __APP_LENGTH - 0x00000410    /* ~511KB */
    CONFIG_HEADER (rx)            : ORIGIN = __CONFIG_HEADER_ADDRESS, LENGTH = __CONFIG_HEADER_LENGTH
    CONFIG (rx)                   : ORIGIN = __CONFIG_ADDRESS,        LENGTH = __CONFIG_LENGTH
    int_sram_results        : ORIGIN = 0x1FFF8000, LENGTH = 0x00000100              /* 256bytes */
    int_sram                : ORIGIN = 0x1FFF8100, LENGTH = 0x0000DF00 - 0x400      /* ~56K */
    int_sram_stack_c0       : ORIGIN = 0x20006000 - 0x400, LENGTH = 0x00001000             /* 4K  */
    ram_rsvd2               : ORIGIN = 0x20007000 - 0x400, LENGTH = 0                       /* End of SRAM */
    ram_reserve             : ORIGIN = 0x20007000 - 0x400, LENGTH = 0x400                   /* End of SRAM */
}


HEAP_SIZE  = DEFINED(__heap_size__)  ? __heap_size__  : 0x00000400;

ENTRY(Reset_Handler)

SECTIONS
{
    .configFLASH __CONFIG_ADDRESS : AT(__CONFIG_ADDRESS)
    {
      . = ALIGN(4);
        KEEP(*(.parameter_config_0))
        KEEP(*(.parameter_config_1))
        KEEP(*(.parameter_config_2))
        KEEP(*(.parameter_config_3))
        KEEP(*(.parameter_config_4))
        KEEP(*(.parameter_config_5))
        KEEP(*(.parameter_config_6))
        KEEP(*(.parameter_config_7))
        KEEP(*(.parameter_config_8))
        KEEP(*(.parameter_config_9))

        KEEP(*(.parameter_config_10))
        KEEP(*(.parameter_config_11))
        KEEP(*(.parameter_config_12))
        KEEP(*(.parameter_config_13))
        KEEP(*(.parameter_config_14))
        KEEP(*(.parameter_config_15))
        KEEP(*(.parameter_config_16))
        KEEP(*(.parameter_config_17))
        KEEP(*(.parameter_config_18))
        KEEP(*(.parameter_config_19))

        KEEP(*(.parameter_config_20))
        KEEP(*(.parameter_config_21))
        KEEP(*(.parameter_config_22))
        KEEP(*(.parameter_config_23))
        KEEP(*(.parameter_config_24))
        KEEP(*(.parameter_config_25))
        KEEP(*(.parameter_config_26))
        KEEP(*(.parameter_config_27))
        KEEP(*(.parameter_config_28))
        KEEP(*(.parameter_config_29))

        KEEP(*(.parameter_config_30))
        KEEP(*(.parameter_config_31))
        KEEP(*(.parameter_config_32))
        KEEP(*(.parameter_config_33))
        KEEP(*(.parameter_config_34))
        KEEP(*(.parameter_config_35))
        KEEP(*(.parameter_config_36))
        KEEP(*(.parameter_config_37))
        KEEP(*(.parameter_config_38))
        KEEP(*(.parameter_config_39))

        KEEP(*(.parameter_config_40))
        KEEP(*(.parameter_config_41))
        KEEP(*(.parameter_config_42))
        KEEP(*(.parameter_config_43))
        KEEP(*(.parameter_config_44))
        KEEP(*(.parameter_config_45))
        KEEP(*(.parameter_config_46))
        KEEP(*(.parameter_config_47))
        KEEP(*(.parameter_config_48))
        KEEP(*(.parameter_config_49))

        KEEP(*(.parameter_config_50))
        KEEP(*(.parameter_config_51))
        KEEP(*(.parameter_config_52))
        KEEP(*(.parameter_config_53))
        KEEP(*(.parameter_config_54))
        KEEP(*(.parameter_config_55))
        KEEP(*(.parameter_config_56))
        KEEP(*(.parameter_config_57))
        KEEP(*(.parameter_config_58))
        KEEP(*(.parameter_config_59))

        KEEP(*(.parameter_config_60))
        KEEP(*(.parameter_config_61))
        KEEP(*(.parameter_config_62))
        KEEP(*(.parameter_config_63))
        KEEP(*(.parameter_config_64))
        KEEP(*(.parameter_config_65))
        KEEP(*(.parameter_config_66))
        KEEP(*(.parameter_config_67))
        KEEP(*(.parameter_config_68))
        KEEP(*(.parameter_config_69))

        KEEP(*(.parameter_config_70))
        KEEP(*(.parameter_config_71))
        KEEP(*(.parameter_config_72))
        KEEP(*(.parameter_config_73))
        KEEP(*(.parameter_config_74))
        KEEP(*(.parameter_config_75))
        KEEP(*(.parameter_config_76))
        KEEP(*(.parameter_config_77))
        KEEP(*(.parameter_config_78))
        KEEP(*(.parameter_config_79))

        KEEP(*(.parameter_config))
        . = ALIGN(4);
    } > CONFIG
}

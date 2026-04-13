MEMORY
{
    int_cflash              : ORIGIN = 0x00500000, LENGTH = 0x001D4000
}

SECTIONS
{
    .configFlash :
    {
        __cflash_start = .;
        KEEP(*(.config_header))
        . = ALIGN(256);
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
        . = ALIGN(128);
        __cflash_end = .;

    } > int_cflash
}

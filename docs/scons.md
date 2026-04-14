# scons

`scons`编译单独编译`config`相关的`c`文件, 然后根据`chcm_config\resources\linker`里面的链接脚本生成`elf`文件以及`hex`和`bin`文件。

## 链接脚本

`chcm_config\resources\linker`里面的链接脚本只保留了配置参数相关的`section`。

## 编译

```powershell
# 编译 a_small 的 config 文件
scons profile=a_small
# 编译 a_plus 的 config 文件
scons profile=a_plus
# 默认编译 a_small
scons
```

## 修改编译内容

在`BUILD_PROFILES`中，`cpppath`和`objects`用来指定需要被编译的文件。

```python
# include path
'cpppath': [
    '../Platform/Common',
    '../Platform/generated',
    '../McuLib/S32K3XX/BaseNXP_TS_T40D34M50I0R0/include',
    '../App/app_swi',
    '../App/app_swi/config',
],
# c 源文件
'objects': [
    {
        'target': 'build/obj/app_config.o',
        'source': '../App/app_config.c',
    },
    {
        'target': 'build/obj/app_swi_config.o',
        'source': '../App/app_swi/config/app_swi_config.c',
    },
],
```

# scons

使用文档。

`scons`编译单独编译`config`相关的`c`文件, 然后根据`chcm_config\resources\linker`里面的链接脚本生成`elf`文件。

`chcm_config\resources\linker`里面的链接脚本只保留了配置参数相关的`section`。

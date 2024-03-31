# verilog模块综合绘图

## 用处

自动读取当前目录所有.v后缀文件，转化成端口图，并放到一个Fig内

帮助理解和快速回忆当时写verilog的思路

## 怎么用

将所有模块的.v文件放到同一个文件夹中，将module_draw.py也放到这个文件夹内，运行这个py文件即可生成模块端口图片。

如图

![image-20240331152608346](README.assets/image-20240331152608346.png)

py生成的模块图如下所示

![image-20240331152625025](README.assets/image-20240331152625025.png)

需要matplotlib和numpy库
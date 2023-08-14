###SJTU (2022-2023)-AI4701 Final Project
----------------------------------------------------------------


####Project framework

> model :保存训练好的模型
>>+ Final_LPRNet_model.pth: 车牌字符识别LPRNet model
>>+ LPRNet.py :LPRNet深度学习网络搭建
>>+ unet.h5: 训练完成的unet模型适用于蓝色车牌识别
>>+ unet_green.h5: 训练完成的unet模型适用于绿色车牌识别

> images: 课程作业要测试的图片
>>+ easy: 简单难度图片
>>+ medium: 中等难度图片
>>+ difficult: 高难度图片

> generateCarPlate-master: 生成虚拟的平面车牌照片当作LPRNet的训练样本
>> + Background: 车牌背景
>> + background2:车牌背景
>> + font: 车牌字体模型
>> + imgs: 生成的车牌照片保存在此
>> + template: 模板照片
>> + genCarPlate.py :生成绿色车牌照片
>> + genCarPlate2.py :生成蓝色车牌照片
>> + PlateCommon.py : 定义生成模型所需的类函数

>data: LPRNet网络读取测试数据以及测试数据加载函数
>> + test: 车牌字符识别LPRNet所识别的照片文件夹
>> + load_data.py: 读取加载函数
>> + NotoSansCJK-Regular.ttc: 保存车牌所用

+ U_net.py: 包含对蓝色车牌进行区域识别的U—net网络定义以及训练、测试函数
+ U_net_green.py: 包含对绿色车牌进行区域识别的U—net网络定义以及训练、测试函数
+ train_LPRNet.py: 训练LPRNet网络
+ test_LPRNet.py: 测试LPRNet网络
+ warp.py: 形态学变换包含生成二值化图、透视投影变换
+ divide.py: 字符分割函数定义
+ extract.py: 对CCPD数据集进行车牌坐标、车牌内容提取
+ main.py: 主函数，对作业照片进行车牌识别
  
####Usage：
main.py 直接运行main函数即可对测试照片进行识别。

U_net.py, U_net_green.py 在path修改所需训练的图片地址，运用load_and_train函数进行读取模型再训练。

generateCarPlate-master：切换终端目录至此文件夹，运行python 终端genCarPlate.py等，添加参数：每个省份分别生成的图片个数，背景所在路径，输出照片路径。
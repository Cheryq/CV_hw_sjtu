import numpy as np
from PIL import Image
import os
import cv2
import tensorflow
from tensorflow.keras import layers, losses, models
from U_net import unet_predict
import matplotlib.pyplot as plt
from divide import divide
from warp import warp
from test_LPRNet import test
def xiugai(image,margin):
    image = warped
    # 获取图片尺寸
    height, width, _ = image.shape

    # 计算新的图片尺寸
    new_height = height - 2 * margin
    new_width = width - 2 * margin

    # 缩小图片
    resized_image = cv2.resize(image, (new_width, new_height))

    # 创建留白的画布
    canvas = np.zeros((height, width, 3), dtype=np.uint8)
    canvas=~canvas
    # 将缩小的图片放置在留白画布上
    canvas[margin:new_height + margin, margin:new_width + margin] = resized_image
    
    return canvas
if __name__ == "__main__":

    blue_model = models.load_model('model/unet.h5')
    green_model = models.load_model('model/unet_green.h5')
    model=[blue_model, green_model]
    color=['blue', 'green']
    img_path='images/'
    filename=['easy/1-1.jpg','easy/1-2.jpg','easy/1-3.jpg','medium/2-1.jpg','medium/2-2.jpg','medium/2-3.jpg','difficult/3-1.jpg','difficult/3-2.jpg','difficult/3-3.jpg']
    t=0
    for i in range(len(filename)):
        path=img_path+filename[i]
        if i>=3:
            if i==7:
                img_src,img_mask=unet_predict(model[1], path)
                warped=warp(color[1], img_src, img_mask)
                
                
            else:
                img_src,img_mask=unet_predict(model[0], path)
                warped=warp(color[0], img_src, img_mask)
                

        else:
            warped=cv2.imread(path)
            if warped.shape != (24, 94, 3):
                warped = cv2.resize(warped, (94, 24))
                warped=xiugai(warped,3)
           
        if warped.shape != (24, 94, 3):
            warped = cv2.resize(warped, (94, 24))
            warped=xiugai(warped,1)
        if len(warped.shape) == 2:
            warped = cv2.merge([warped]*3)
        cv2.imwrite('data/test/{}.jpg'.format(t), warped)
        t+=1
    test()

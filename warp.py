import numpy as np
import os
import cv2
import tensorflow
from tensorflow.keras import layers, losses, models
from divide import divide
import matplotlib.pyplot as plt
from U_net import unet_predict

def warp(color,img_src,img_mask):
    
    gray = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    mask_gray=cv2.cvtColor(img_mask, cv2.COLOR_BGR2GRAY)
    mask_thresh=cv2.threshold(mask_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    mask_thresh=~mask_thresh

    contours, hierarchy = cv2.findContours(mask_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 过滤出符合条件的轮廓
    candidates = []
    for cnt in contours:
        # 计算轮廓的周长和面积
        perimeter = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)
        # 过滤掉面积和周长不符合要求的轮廓
        if area > 200 and perimeter > 100:
            # 进行轮廓近似，得到一个包含所有白色像素的平行四边形轮廓
            approx = cv2.approxPolyDP(cnt, 0.03 * perimeter, True)
            if len(approx) == 4:
                candidates.append(approx)

    #将所有符合条件的轮廓画在图像上
    #cv2.drawContours(img_src, candidates, -1, (0, 255, 0), 2)
    #cv2.imshow('Source Image', img_src)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    vertices = []
    assert len(candidates) > 0, "No candidates found"
    for point in candidates[0]:
        x = point[0][0]
        y = point[0][1]
        vertices.append([x, y])
    
    
    # 对坐标点进行排序
    sorted_vertices = sorted(vertices, key=lambda point: point[1])
    top_points = sorted(sorted_vertices[:2], key=lambda point: point[0])
    bottom_points = sorted(sorted_vertices[2:], key=lambda point: -point[0])
    if color=='green':
        top_points[0][1]-=3
        bottom_points[1][0]-=3
    sorted_vertices = top_points + bottom_points

    # 计算变换前后的四个点坐标
    src_pts = np.float32(sorted_vertices)
    dst_pts = np.float32([(0, 0), (440,0),(440,140),(0,140)])

    # 计算变换矩阵
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)

    # 对原始图像进行变换
    warped = cv2.warpPerspective(img_src, M, (440, 140))
    
    
    #character_mean = warped.mean()
    #if character_mean>125:
    #    warped=~warped
    
    
    return warped

'''blue_model = models.load_model('unet.h5')
img_src,img_mask=unet_predict(blue_model, 'resources/images/difficult/3-1.jpg')
warped=warp('blue', img_src, img_mask)
word=divide(warped)
for i,j in enumerate(word):
    plt.subplot(1,9,i+1)
    plt.imshow(word[i],cmap='gray')
plt.show()'''
    
    
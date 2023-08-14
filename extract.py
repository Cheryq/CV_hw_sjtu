import os
import cv2
import numpy as np
def extract_dir_data(data_dir):
    #车牌字典
    #省
    provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤",
                    "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]
    #具体信息
    word_lists = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                    'W','X', 'Y', 'Z', 'O', '1', '2', '3', '4', '5', '6', '7', '8', '9','0']


    data_dir = 'train'  # 数据集所在目录
    area_list = []
    num_list = []
    for file_name in os.listdir(data_dir):
        if file_name.endswith('.jpg'):
            img_path = os.path.join(data_dir, file_name)
        
            # 从文件名中提取车牌标注框坐标
            fields = file_name.split('-')
            area = tuple(map(int, fields[2].replace('&', '_').split('_')))
            left_top = tuple(area[0:2])
            right_bottom = tuple(area[2:4])
            
            area_list.append([left_top[0], left_top[1], right_bottom[0], right_bottom[1]])
            # 从文件名中提取车牌号码
            num_str = fields[4].split('_')
            num = [provinces[int(num_str[0])]]
            for i in range(1, len(num_str)):
                num.append(word_lists[int(num_str[i])])
            num_list.append(num)

            # 显示提取结果
            #img = cv2.imread(img_path)
            #cv2.rectangle(img, left_top, right_bottom, (0, 255, 0), 2)
            #cv2.imshow('result', img)
            #cv2.waitKey(0)

    area_train = np.array(area_list)
    num_train = np.array(num_list)
    return area_train, num_train
def extract_img_data(file_name):
     #车牌字典
    #省
    provinces = ["皖", "沪", "津", "渝", "冀", "晋", "蒙", "辽", "吉", "黑", "苏", "浙", "京", "闽", "赣", "鲁", "豫", "鄂", "湘", "粤",
                    "桂", "琼", "川", "贵", "云", "藏", "陕", "甘", "青", "宁", "新", "警", "学", "O"]
    #具体信息
    word_lists = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                    'W','X', 'Y', 'Z', 'O', '1', '2', '3', '4', '5', '6', '7', '8', '9','0']
    # 从文件名中提取车牌标注框坐标
    fields = file_name.split('-')
    area = tuple(map(int, fields[3].replace('&', '_').split('_')))
    area=np.array(area)
    # 从文件名中提取车牌号码
    num_str = fields[4].split('_')
    num = [provinces[int(num_str[0])]]
    for i in range(1, len(num_str)):
        num.append(word_lists[int(num_str[i])])
    num_res=np.array(num)
    return area, num_res


def get_label(file_name,color):
    if (color==0):
        path = 'img/blue/train/'
    elif (color==1):
        path = 'img/green/train/'
    area, num_res = extract_img_data(file_name)

    # 构造全黑色图像
    img = cv2.imread(path + file_name)
    mask = np.zeros_like(img[:, :, :], dtype=np.uint8)

    right_bottom = tuple(area[0:2])
    left_bottom = tuple(area[2:4])
    left_top = tuple(area[4:6])
    right_top = tuple(area[6:8])

    # 用白色填充平行四边形区域
    pts = np.array([right_bottom, left_bottom, left_top, right_top])
    cv2.fillPoly(mask, [pts], (255, 255, 255))
   
    #显示结果
    #cv2.imshow('result', mask)
    #cv2.waitKey(0)

    return mask

    
    # 将原图转化为灰度图像并进行二值化处理
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # 将白色车牌区域图像与二值化图像进行逻辑与操作
    #result = cv2.bitwise_and(thresh, thresh, mask=mask)
    
    # 显示结果
    #cv2.imshow('result', result)
    #cv2.waitKey(0)


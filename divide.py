import cv2

def divide(img):
    img_thre=img
    white = []  # 记录每一列的白色像素总和
    black = []  # ..........黑色.......
    height = img_thre.shape[0]
    width = img_thre.shape[1]
    white_max = 0
    black_max = 0
    # 计算每一列的黑白色像素总和
    for i in range(width):
        s = 0  # 这一列白色总数
        t = 0  # 这一列黑色总数
        for j in range(height):
            if img_thre[j][i] > 200:
                s += 1
            if img_thre[j][i] < 50:
                t += 1
        white_max = max(white_max, s)
        black_max = max(black_max, t)
        white.append(s)
        black.append(t)
        # print(s)
        # print(t)

    arg = False  # False表示白底黑字；True表示黑底白字
    if black_max > white_max:
        arg = True

    # 分割图像
    def find_end(start_):
        end_ = start_ + 1
        for m in range(start_ + 1, width - 1):
            if (black[m] if arg else white[m]) > (0.9 * black_max if arg else 0.95 * white_max):  # 0.95这个参数请多调整，对应下面的0.05（针对像素分布调节）
                end_ = m
                break
        return end_

    n = 1
    start = 1
    end = 2
    word = []
    while n < width - 2:
        n += 1
        if (white[n] if arg else black[n]) > (0.1 * white_max if arg else 0.05 * black_max):
            # 上面这些判断用来辨别是白底黑字还是黑底白字
            # 0.05这个参数请多调整，对应上面的0.95
            start = n
            end = find_end(start)
            n = end
            if end - start > 5:
                cj = img[1:height, start:end]
                cj = cv2.resize(cj, (15, 30))
                word.append(cj)
    return word


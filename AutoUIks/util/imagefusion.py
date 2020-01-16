#coding:utf-8
import numpy as np
import cv2
def image_fusion(imagelist):
    leftgray = cv2.imread(imagelist[1])
    #leftgray = cv2.imdecode(np.fromfile(imagelist[1], dtype=np.uint8), -1)
    rightgray = cv2.imread(imagelist[2])
    hessian = 400
    surf = cv2.xfeatures2d.SURF_create(hessian)   # 将Hessian Threshold设置为400,阈值越大能检测的特征就越少
    print(leftgray)
    kp1, des1 = surf.detectAndCompute(leftgray, None)  # 查找关键点和描述符
    kp2, des2 = surf.detectAndCompute(rightgray, None)

    FLANN_INDEX_KDTREE = 0  # 建立FLANN匹配器的参数
    indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)  # 配置索引，密度树的数量为5
    searchParams = dict(checks=50)  # 指定递归次数
    # FlannBasedMatcher：是目前最快的特征匹配算法（最近邻搜索）
    flann = cv2.FlannBasedMatcher(indexParams, searchParams)  # 建立匹配器
    matches = flann.knnMatch(des1, des2, k=2)  # 得出匹配的关键点

    good = []
    # 提取优秀的特征点
    for m, n in matches:
        if m.distance < 0.7 * n.distance:  # 如果第一个邻近距离比第二个邻近距离的0.7倍小，则保留
            good.append(m)
    src_pts = np.array([kp1[m.queryIdx].pt for m in good])  # 查询图像的特征描述子索引
    dst_pts = np.array([kp2[m.trainIdx].pt for m in good])  # 训练(模板)图像的特征描述子索引
    H = cv2.findHomography(src_pts, dst_pts)  # 生成变换矩阵
    h, w = leftgray.shape[:2]
    h1, w1 = rightgray.shape[:2]
    #shft = np.array([[1.0, 0, w], [0, 1.0, 0], [0, 0, 1.0]])
    shft = np.array([[1.0, 0, 0], [0, 1.0, h], [0, 0, 1.0]])
    M = np.dot(shft, H[0])  # 获取左边图像到右边图像的投影映射关系
    dst_corners = cv2.warpPerspective(leftgray, M, (w, h*2))  # 透视变换，新图像可容纳完整的两幅图
    dst_corners[0:h, 0:w] = leftgray  # 将第二幅图放在右侧
    #cv2.imshow('tiledImg1', dst_corners)  # 显示，第一幅图已在标准位置
    cv2.imwrite('./image/tiledImg1.png', dst_corners)
    dst_corners[h:h * 2, 0:w] = rightgray  # 将第二幅图放在右侧
    cv2.imwrite('./image/tiledImg2.png',dst_corners)
    # cv2.imshow('tiledImg', dst_corners)
    # cv2.imshow('leftgray', leftgray)
    # cv2.imshow('rightgray', rightgray)
    cv2.waitKey()
    #cv2.destroyAllWindows()


if __name__ =='__main__':
    imagelist = [ './image/result0.png',
                 './image/result1.png',
                 './image/result2.png',
                 './image/result3.png',]
    image_fusion(imagelist)

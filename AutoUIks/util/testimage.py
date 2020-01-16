#coding:utf-8
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import cv2
def image_fusion(imagelist):
    # leftgray = cv2.imdecode(np.fromfile(imagelist[1], dtype=np.uint8), -1)
    leftgray = cv2.imread(imagelist[1])
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

def test(imagelist):
    top, bot, left, right = 100, 100, 0, 500
    img1 = cv.imread(imagelist[1])
    img2 = cv.imread(imagelist[2])
    srcImg = cv.copyMakeBorder(img1, top, bot, left, right, cv.BORDER_CONSTANT, value=(0, 0, 0))
    testImg = cv.copyMakeBorder(img2, top, bot, left, right, cv.BORDER_CONSTANT, value=(0, 0, 0))
    img1gray = cv.cvtColor(srcImg, cv.COLOR_BGR2GRAY)
    img2gray = cv.cvtColor(testImg, cv.COLOR_BGR2GRAY)
    # img1gray = cv2.imread(imagelist[1])
    # img2gray = cv2.imread(imagelist[2])
    sift = cv.xfeatures2d_SIFT().create()
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1gray, None)
    kp2, des2 = sift.detectAndCompute(img2gray, None)
    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]

    good = []
    pts1 = []
    pts2 = []
    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            good.append(m)
            pts2.append(kp2[m.trainIdx].pt)
            pts1.append(kp1[m.queryIdx].pt)
            matchesMask[i] = [1, 0]

    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matchesMask,
                       flags=0)
    img3 = cv.drawMatchesKnn(img1gray, kp1, img2gray, kp2, matches, None, **draw_params)
    plt.imshow(img3, ), plt.show()

    rows, cols = srcImg.shape[:2]
    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
        warpImg = cv.warpPerspective(testImg, np.array(M), (testImg.shape[1], testImg.shape[0]),
                                     flags=cv.WARP_INVERSE_MAP)

        for col in range(0, cols):
            if srcImg[:, col].any() and warpImg[:, col].any():
                left = col
                break
        for col in range(cols - 1, 0, -1):
            if srcImg[:, col].any() and warpImg[:, col].any():
                right = col
                break

        res = np.zeros([rows, cols, 3], np.uint8)
        for row in range(0, rows):
            for col in range(0, cols):
                if not srcImg[row, col].any():
                    res[row, col] = warpImg[row, col]
                elif not warpImg[row, col].any():
                    res[row, col] = srcImg[row, col]
                else:
                    srcImgLen = float(abs(col - left))
                    testImgLen = float(abs(col - right))
                    alpha = srcImgLen / (srcImgLen + testImgLen)
                    res[row, col] = np.clip(srcImg[row, col] * (1 - alpha) + warpImg[row, col] * alpha, 0, 255)

        # opencv is bgr, matplotlib is rgb
        res = cv.cvtColor(res, cv.COLOR_BGR2RGB)
        # show the result
        plt.figure()
        plt.imshow(res)
        plt.show()
    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        matchesMask = None


if __name__ =='__main__':
    imagelist = [ './image/result0.png',
                 './image/test1.jpg',
                 './image/test2.jpg',
                 './image/result3.png',]
    #image_fusion(imagelist)
    test(imagelist)

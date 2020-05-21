import cv2
import numpy as np

global img
global point1, point2

lsPointsChoose = []
tpPointsChoose = []


def on_mouse(event, x, y, flags, param):
    global img, point1, point2
    global lsPointsChoose, tpPointsChoose  # 存入选择的点
    global init_img, ROI_bymouse_flag
    init_img = img.copy()  # 此行代码保证每次都重新再原图画 避免画多了

    if event == cv2.EVENT_LBUTTONDOWN:  # 左键点击
        point1 = (x, y)
        # 画出点击的点
        cv2.circle(init_img, point1, 1, (255, 255, 255), 1)

        # 将选取的点保存到list列表里
        lsPointsChoose.append([x, y])  # 用于转化为darry 提取多边形ROI
        tpPointsChoose.append((x, y))  # 用于画点

        # 将鼠标选的点用直线链接起来
        print(len(tpPointsChoose))
        for i in range(len(tpPointsChoose) - 1):
            cv2.line(init_img, tpPointsChoose[i], tpPointsChoose[i + 1], (255, 255, 255), 2)

        cv2.imshow('src', init_img)

    # 右键结束抠图
    if event == cv2.EVENT_RBUTTONDOWN:  # 右键点击
        # 绘制感兴趣区域
        ROI_byMouse()
        ROI_bymouse_flag = 1
        lsPointsChoose = []
        cv2.destroyAllWindows()


def ROI_byMouse():
    global src, ROI, ROI_flag, mask2
    mask = np.zeros(img.shape, np.uint8)
    pts = np.array([lsPointsChoose], np.int32)

    pts = pts.reshape((-1, 1, 2))  # -1代表剩下的维度自动计算

    # 画多边形
    mask = cv2.polylines(mask, [pts], True, (0, 255, 255))
    # 填充多边形
    mask2 = cv2.fillPoly(mask, [pts], (255, 255, 255))
    ROI = cv2.bitwise_and(mask2, img)
    cv2.imwrite(path, ROI)


def main(get_path):
    global img, init_img, ROI, path
    path = get_path
    img = cv2.imread(path)
    # 图像预处理，设置其大小
    height, width = img.shape[:2]
    img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
    ROI = img.copy()
    cv2.namedWindow('src')
    cv2.setMouseCallback('src', on_mouse)
    cv2.imshow('src', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()

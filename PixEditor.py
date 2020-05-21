# -*- coding: utf-8 -*-
# @Time    : 2020/5/11 9:14
# @Author  : Arcgo
# @FileName: PixEditor.py
# @Software: PixEditor
# @Blog    ：https://blog.csdn.net/Arcgo

import os
import shutil
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QColorDialog, QApplication
from matplotlib import pyplot as plt
import ChangeFace
import ManuCutout
import Cut
import UI
import AutoCutout
from Color import *
from Denoise import *
from Filter import *
from Lighting import *
from Portrait import *
from Text import *
from Draw import *


class MainCode(QMainWindow, UI.Ui_MainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        UI.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(0)
        if not (os.path.exists("process")):
            os.makedirs("process")

        # 程序启动即初始化栈数据结构
        global s
        s = Stack()
        s.__init__()

        global lig
        lig = Lighting()

        global col
        col = Color()

        # 打开
        self.open_.clicked.connect(self.open)
        # 储存
        self.save_.clicked.connect(self.save)
        # 重置按钮
        self.reset_.clicked.connect(self.reset)
        # 撤销按钮
        self.undo_.clicked.connect(self.undo)
        # 裁剪
        self.btn_cut.clicked.connect(self.cut_)
        # 旋转
        self.rotate.clicked.connect(self.page_rotate_show)
        self.rotate_ensure.clicked.connect(self.rotate_)

        # 分页
        self.editor.clicked.connect(self.page_0_show)
        self.btn_text.clicked.connect(self.page_1_show)
        self.btn_denoise.clicked.connect(self.page_2_show)
        self.btn_statistic.clicked.connect(self.page_3_show)
        self.btn_filter.clicked.connect(self.page_4_show)
        self.btn_cutout.clicked.connect(self.page_5_show)
        self.btn_face.clicked.connect(self.page_6_show)
        self.btn_sticker.clicked.connect(self.page_7_show)
        self.btn_change_face.clicked.connect(self.page_8_show)
        self.filter_more.clicked.connect(self.page_9_show)
        self.filter_back.clicked.connect(self.page_4_show)

        # 光效
        self.brightness.sliderReleased.connect(self.bright_)
        self.contrast.sliderReleased.connect(self.contrast_)
        self.sharpness.sliderReleased.connect(self.sharpness_)
        # 色彩
        self.saturate.sliderReleased.connect(self.saturate_)

        # 直方图
        self.btn_rgb.clicked.connect(self.showRGB)
        self.btn_pixel.clicked.connect(self.showPixel)

        # 降噪
        self.btn_gaussian.clicked.connect(self.gaussian_)
        self.btn_blur.clicked.connect(self.blur_)
        self.btn_smooth_more.clicked.connect(self.smooth_more_)

        # 文字
        self.text_color.clicked.connect(self.text_color_)
        self.textEnsure.clicked.connect(self.text_)

        # 滤镜
        self.filter_pencil.clicked.connect(self.pencil)
        self.filter_emboss.clicked.connect(self.emboss)
        self.filter_blur.clicked.connect(self.blur__)
        self.filter_smooth.clicked.connect(self.smooth)
        self.filter_sharpen.clicked.connect(self.sharpen)
        self.filter_edge.clicked.connect(self.edge)
        self.filter_sunny.clicked.connect(lambda :self.filter_more_("sunny"))
        self.filter_trip.clicked.connect(lambda: self.filter_more_("trip"))
        self.filter_sakura.clicked.connect(lambda: self.filter_more_("sakura"))
        self.filter_jiangnan.clicked.connect(lambda: self.filter_more_("jiang_nan"))
        self.filter_wangjiawei.clicked.connect(lambda: self.filter_more_("wangjiawei"))
        self.filter_prague.clicked.connect(lambda: self.filter_more_("prague"))

        # 抠图
        self.cutout_auto.clicked.connect(self.autocutout_)
        self.cutout_manu.clicked.connect(self.manucutout_)

        # 人像
        self.face_ensure.clicked.connect(self.face_)

        # 贴图
        self.stick_select.clicked.connect(self.stick_open)
        self.stick_ensure.clicked.connect(self.stick_)

        # 换脸
        self.change_face_select.clicked.connect(self.change_face_open)
        self.change_face_ensure.clicked.connect(self.changeface_)

    # 打开
    def open(self):
        # 获取文件名及类型
        filename, filetype = QFileDialog.getOpenFileName(self, "打开文件", "C:",
                                                         "Files(*.png; *.jpg; *.jpeg; *.bmp; *.gif;)")
        if not filename == "":
            # 将打开的文件压入栈中
            s.push(filename)
            # 在lable中展示
            self.show_()

    # 储存
    def save(self):
        # 被保存的文件的路径
        path = s.peek()
        # 栈中有元素时
        if not path == None:
            img = Image.open(path)
            # 保存的路径
            save_path, file_type = QFileDialog.getSaveFileName(self, "文件保存", "C:",
                                                               "All Files (*);;Files (*.png);;Files (*.jpg);;Files ("
                                                               "*.jpeg);;Files (*.bmp);;Files (*.gif)")
            if not save_path == "":
                img.save(save_path)

    # 分页
    # 光效页
    def page_0_show(self):
        self.stackedWidget.setCurrentIndex(0)

    # 文字页
    def page_1_show(self):
        self.stackedWidget.setCurrentIndex(1)

    # 降噪页
    def page_2_show(self):
        self.stackedWidget.setCurrentIndex(2)

    # 统计页
    def page_3_show(self):
        self.stackedWidget.setCurrentIndex(3)

    # 滤镜页
    def page_4_show(self):
        self.stackedWidget.setCurrentIndex(4)

    # 抠图页
    def page_5_show(self):
        self.stackedWidget.setCurrentIndex(5)

    # 人像页
    def page_6_show(self):
        self.stackedWidget.setCurrentIndex(6)

    # 贴图页
    def page_7_show(self):
        self.stackedWidget.setCurrentIndex(7)

    # 换脸页
    def page_8_show(self):
        self.stackedWidget.setCurrentIndex(8)

    # 更多滤镜页
    def page_9_show(self):
        self.stackedWidget.setCurrentIndex(9)

    # 旋转页
    def page_rotate_show(self):
        self.stackedWidget_2.setCurrentIndex(1)

    # 展示图片
    def show_(self):
        # 获取此时栈顶元素
        path = s.peek()
        img = Image.open(path)
        img_type = img.format
        width, height = img.size
        if img_type == "PNG" or "JPG" or "BMP" or "JPEG":
            if width <= 1200 and height <= 750:
                # 居中显示图片
                self.display.setAlignment(Qt.AlignCenter)
                self.display.setPixmap(QPixmap(path))
            # 等比例压缩图片
            else:
                f1 = 1.0 * 1200 / width
                f2 = 1.0 * 750 / height
                factor = min(f1, f2)
                new_width = int(width * factor)
                new_height = int(height * factor)
                self.make_duplicate()
                img = Image.open(s.peek())
                out = img.resize((new_width, new_height), Image.ANTIALIAS)
                out.save(s.peek())
                self.display.setAlignment(Qt.AlignCenter)
                self.display.setPixmap(QPixmap(s.peek()))

        if img_type == "GIF":
            self.movie = QMovie(s.peek())
            self.display.setMovie(self.movie)
            self.movie.start()

    # 重置图片
    def reset(self):
        if not s.is_empty():
            if not s.size() == 1:
                s.reset()
                self.show_()

    # 撤销
    def undo(self):
        if not s.is_empty():
            if not s.size() == 1:
                # 删除栈顶元素
                s.pop()
                self.show_()

    # 为栈顶文件制作副本
    def make_duplicate(self):
        # 复制当前栈顶文件到img
        img = Image.open(s.peek())
        # 获得文件名并重新制作为 文件名 + (1) + .格式
        filename = s.peek()
        filename = filename.split("/")
        filename = filename[-1]
        filename = filename.split(".")
        filename = filename[0] + "(1)" + "." + filename[-1]
        # 副本的储存路径 = process/(相对路径) + 重新制作后的文件名
        path = "process/" + filename
        # 储存副本
        img.save(path)
        # 副本文件的路径入栈
        s.push(path)

    # 功能接口区
    # 缩放接口
    def wheelEvent(self, event):
        if not s.is_empty():
            self.make_duplicate()
            path = s.peek()
            angle = event.angleDelta() / 8
            angleY = angle.y()  # 竖直滚过的距离
            if angleY > 0:
                img = QImage(path)
                result = img.scaled(img.width() * 1.1, img.height() * 1.1)
                self.display.setPixmap(QPixmap(result))
                result.save(path)

            else:  # 滚轮下滚
                img = QImage(path)
                result = img.scaled(img.width() * 0.9, img.height() * 0.9)
                self.display.setPixmap(QPixmap(result))
                result.save(path)

    # 裁剪接口
    def cut_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            Cut.main(path)
            self.show_()

    # 旋转接口
    def rotate_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            angle = self.rotate_angle.value()
            img = Image.open(path)
            outcome = img.rotate(angle)
            outcome.save(path)
            self.show_()

    # 光效接口
    def bright_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            value = self.brightness.value()
            lig.bright(path, value)
            self.show_()

    def contrast_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            value = self.contrast.value()
            lig.contrast(path, value)
            self.show_()

    def sharpness_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            value = self.sharpness.value()
            lig.sharpness(path, value)
            self.show_()

    # 色彩接口
    def saturate_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            value = self.saturate.value()
            col.saturate(path, value)
            self.show_()

    # 降噪接口
    def gaussian_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            den = Denoise()
            den.gaussian(path)
            self.show_()

    def blur_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            den = Denoise()
            den.blur(path)
            self.show_()

    def smooth_more_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            den = Denoise()
            den.smooth_more(path)
            self.show_()

    # 直方图
    def showRGB(self):
        if s.is_empty():
            self.open()
        else:
            img = cv.imread(s.peek(), cv.IMREAD_COLOR)
            color_ = ('b', 'g', 'r')
            for i, colors in enumerate(color_):
                histr = cv.calcHist([img], [i], None, [256], [0, 256])
                plt.plot(histr, color=colors)
            plt.xlim([0, 256])
            plt.show()

    def showPixel(self):
        if s.is_empty():
            self.open()
        else:
            p = cv.imread(s.peek(), -1)
            plt.hist(p.ravel(), 256, [0, 256])
            plt.show()
            cv.waitKey(0)
            cv.destroyAllWindows()

    # 文字接口
    def text_color_(self):
        global text_r, text_g, text_b
        color = QColorDialog.getColor()
        if color.isValid():
            temp = color.name()
            temp = temp[1:]
            text_r = int(temp[0:2], 16)
            text_g = int(temp[2:4], 16)
            text_b = int(temp[4:6], 16)

    def text_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            content = self.textEdit.toPlainText()
            fontScale = int(self.text_fontScale.value())
            color = (text_b, text_g, text_r)
            x = int(self.text_x.toPlainText())
            y = int(self.text_y.toPlainText())
            thickness = int(self.text_thickess.value())
            txt = Text()
            txt.addText(path, content, fontScale, x, y, color, thickness)
            self.show_()

    # 滤镜接口
    def pencil(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            flt = Filter()
            flt.pencil(path)
            self.show_()

    def emboss(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            flt = Filter()
            flt.emboss(path)
            self.show_()

    def blur__(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            flt = Filter()
            flt.blur(path)
            self.show_()

    def smooth(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            flt = Filter()
            flt.smooth(path)
            self.show_()

    def edge(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            flt = Filter()
            flt.edge(path)
            self.show_()

    def sharpen(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            flt = Filter()
            flt.sharpen(path)
            self.show_()

    def filter_more_(self, filter_type):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            flt = Filter()
            flt.filter_more(path, filter_type)
            self.show_()

    # 抠图接口
    def autocutout_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            co = AutoCutout
            co.AutoCutout(path)
            self.show_()

    def manucutout_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            ManuCutout.main(path)
            self.show_()

    # 人像接口
    def face_(self):
        if s.is_empty():
            self.open()
        else:
            self.make_duplicate()
            path = s.peek()
            whitening = self.whitening.value()
            smoothing = self.smoothing.value()
            thinface = self.thinface.value()
            shrink_face = self.shrink_face.value()
            enlarge_eye = self.enlarge_eye.value()
            remove_eyebrow = self.remove_eyebrow.value()
            p = Portrait()
            p.face_beautify(path, whitening, smoothing, thinface, shrink_face, enlarge_eye, remove_eyebrow)
            self.show_()

    # 贴图接口
    def stick_open(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "打开文件", "C:",
                                                         "Files(*.png; *.jpg; *.jpeg; *.bmp; *.gif;)")
        self.stick_address.setPlainText(filename)

    def stick_(self):
        path_stick = self.stick_address.toPlainText()
        if path_stick == "":
            self.stick_open()
        else:
            self.make_duplicate()
            path = s.peek()
            x = int(self.stick_x.toPlainText())
            y = int(self.stick_y.toPlainText())
            img1 = Image.open(path)
            img2 = Image.open(path_stick)
            img1.paste(img2, (x, y))
            img1.save(path)
            self.show_()

    # 换脸接口
    def change_face_open(self):
        filename, filetype = QFileDialog.getOpenFileName(self, "打开文件", "C:",
                                                         "Files(*.png; *.jpg; *.jpeg; *.bmp; *.gif;)")
        self.change_face_address.setPlainText(filename)

    def changeface_(self):
        path_change_face = self.change_face_address.toPlainText()
        if path_change_face == "":
            self.change_face_open()
        else:
            self.make_duplicate()
            path = s.peek()
            cf = ChangeFace
            cf.merge_face(path, path_change_face)
            self.show_()

    def closeEvent(self, event):
        if os.path.exists("process"):
            shutil.rmtree("process")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    md = MainCode()

    # 画笔子窗口
    draw_window = MainWidget()
    md.btn_draw.clicked.connect(draw_window.show)

    md.show()

    sys.exit(app.exec_())

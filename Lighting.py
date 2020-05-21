from PIL import Image, ImageEnhance
from Stack import *


class Lighting:

    # 创建栈
    def __init__(self):
        global s
        s = Stack()
        s.__init__()

    # 亮度接口：目的为每次改变是基于第一次传入的图片(栈底的图片)
    def bright(self, path, value):
        # 判断栈s是否为空。若空则path直接入栈
        if s.is_empty():
            s.push(path)
            outcome = self.bright_func(path, value)
            outcome.save(path)
        else:
            # 制作路径判断，检查是否为同一组图片
            ori_path = s.peek()
            ori_path = ori_path.split(".")
            gues_path = ori_path[-2]
            gues_path2 = gues_path + "(1)" + "." + ori_path[-1]
            s.push(gues_path2)

            # 当是同一图片连续修改时，传入原图而非修改后的图片
            if path == gues_path2:
                outcome = self.bright_func(s.get_base(), value)
                outcome.save(path)
            # 当不是连续修改时(传入新的图片)，则清空栈
            else:
                s.empty()
                s.push(path)
                outcome = self.bright_func(s.get_base(), value)
                outcome.save(path)

    # 对比度接口
    def contrast(self, path, value):
        if s.is_empty():
            s.push(path)
            outcome = self.contrast_func(path, value)
            outcome.save(path)
        else:
            # 制作路径判断
            ori_path = s.peek()
            ori_path = ori_path.split(".")
            gues_path = ori_path[-2]
            gues_path2 = gues_path + "(1)" + "." + ori_path[-1]
            s.push(gues_path2)

            # 当是连续修改时，传入原图而非修改后的图片
            if path == gues_path2:
                outcome = self.contrast_func(s.get_base(), value)
                outcome.save(path)
            # 当不是连续修改时(传入新的图片)，则清空栈
            else:
                s.empty()
                s.push(path)
                outcome = self.contrast_func(s.get_base(), value)
                outcome.save(path)

    # 锐度接口
    def sharpness(self, path, value):
        if s.is_empty():
            s.push(path)
            outcome = self.sharpness_func(path, value)
            outcome.save(path)
        else:
            # 制作路径判断
            ori_path = s.peek()
            ori_path = ori_path.split(".")
            gues_path = ori_path[-2]
            gues_path2 = gues_path + "(1)" + "." + ori_path[-1]
            s.push(gues_path2)

            # 当是连续修改时，传入原图而非修改后的图片
            if path == gues_path2:
                outcome = self.sharpness_func(s.get_base(), value)
                outcome.save(path)
            # 当不是连续修改时(传入新的图片)，则清空栈
            else:
                s.empty()
                s.push(path)
                outcome = self.sharpness_func(s.get_base(), value)
                outcome.save(path)

    # 亮度实际功能
    def bright_func(self, path, value):
        img = Image.open(path)
        enh_bri = ImageEnhance.Brightness(img)
        outcome = enh_bri.enhance(value/10)
        return outcome

    # 对比度实际功能
    def contrast_func(self, path, value):
        img = Image.open(path)
        enh_con = ImageEnhance.Contrast(img)
        outcome = enh_con.enhance(value/10)
        return outcome

    # 锐度实际功能
    def sharpness_func(self, path, value):
        img = Image.open(path)
        enh_sha = ImageEnhance.Sharpness(img)
        outcome = enh_sha.enhance(value/10)
        return outcome
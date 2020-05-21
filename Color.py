from PIL import Image
from PIL import ImageEnhance
from Stack import *


class Color:

    # 创建栈
    def __init__(self):
        global s
        s = Stack()
        s.__init__()

    # 饱和度接口：目的为每次改变是基于第一次传入的图片(栈底的图片)
    def saturate(self, path, value):
        if s.is_empty():
            s.push(path)
            outcome = self.saturate_func(path, value)
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
                outcome = self.saturate_func(s.get_base(), value)
                outcome.save(path)
            # 当不是连续修改时(传入新的图片)，则清空栈
            else:
                s.empty()
                s.push(path)
                outcome = self.saturate_func(s.get_base(), value)
                outcome.save(path)

    # 饱和度功能
    def saturate_func(self, path, value):
        img = Image.open(path)
        enh_col = ImageEnhance.Color(img)
        outcome = enh_col.enhance(value/10)
        return outcome

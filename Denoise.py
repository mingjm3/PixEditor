from PIL import Image, ImageFilter


# 降噪功能模块，处理后按照传入路径覆盖式输出图片

class Denoise():

    # 均值模糊
    def blur(self, path):
        img = Image.open(path)
        outcome = img.filter(ImageFilter.BLUR)
        outcome.save(path)

    # 高斯模糊
    def gaussian(self, path):
        img = Image.open(path)
        outcome = img.filter(ImageFilter.GaussianBlur)
        outcome.save(path)

    # 柔和
    def smooth_more(self, path):
        img = Image.open(path)
        outcome = img.filter(ImageFilter.SMOOTH_MORE)
        outcome.save(path)


from PIL import Image, ImageFilter
from json import JSONDecoder
import requests
import base64


class Filter:

    # 铅笔滤镜
    def pencil(self, path):
        img = Image.open(path)
        outcome = img.filter(ImageFilter.CONTOUR)
        outcome.save(path)

    # 浮雕滤镜
    def emboss(self, path):
        img = Image.open(path)
        outcome = img.filter(ImageFilter.EMBOSS)
        outcome.save(path)

    # 朦胧滤镜
    def blur(self, path):
        img = Image.open(path)
        outcome = img.filter(ImageFilter.BLUR)
        outcome.save(path)

    # 平滑滤镜
    def smooth(self, path):
        img = Image.open(path)
        outcome = img.filter(ImageFilter.SMOOTH)
        outcome.save(path)

    # 边缘滤镜
    def edge(self, path):
        img = Image.open(path)
        outcome = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        outcome.save(path)

    # 锐化滤镜
    def sharpen(self, path):
        img = Image.open(path)
        outcome = img.filter(ImageFilter.SHARPEN)
        outcome.save(path)

    # 更多滤镜
    def filter_more(self, path, filter_type):
        http_url = "https://api-cn.faceplusplus.com/facepp/v2/beautify"
        key = "Dwv3vykUxETEuoZGQeX5f52P_J459yLA"
        secret = "fvQgHRehl7sGrkFeJcG0xiUEd2y2NjqG"

        data = {"api_key": key, "api_secret": secret, "whitening": 0, "smoothing": 0,
                "thinface": 0, "shrink_face": 0, "enlarge_eye": 0,
                "remove_eyebrow": 0, "filter_type": filter_type}
        files = {"image_file": open(path, "rb")}

        response = requests.post(http_url, data=data, files=files)
        req_con = response.content.decode('utf-8')
        req_dict = JSONDecoder().decode(req_con)
        result = req_dict['result']
        # 对其解码成字典格式
        imgdata = base64.b64decode(result)
        file = open(path, 'wb')
        file.write(imgdata)
        file.close()

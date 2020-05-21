from json import JSONDecoder
import requests
import base64


class Portrait:
    def face_beautify(self, path, whitening, smoothing, thinface, shrink_face, enlarge_eye, remove_eyebrow):
        http_url = "https://api-cn.faceplusplus.com/facepp/v2/beautify"
        key = "Dwv3vykUxETEuoZGQeX5f52P_J459yLA"
        secret = "fvQgHRehl7sGrkFeJcG0xiUEd2y2NjqG"

        data = {"api_key": key, "api_secret": secret, "whitening": whitening, "smoothing": smoothing,
                "thinface": thinface, "shrink_face": shrink_face, "enlarge_eye": enlarge_eye,
                "remove_eyebrow": remove_eyebrow}
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

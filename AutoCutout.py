import cv2
import base64
import numpy as np

from aip import AipBodyAnalysis


def AutoCutout(path):
    APP_ID = '19815134'
    API_KEY = 'i7yBb3Fx3e4ZMILo8nHsrZQT'
    SECRET_KEY = 'wuEXaPYbz1RXlAdDYYRj49tlPoNZdqfW'

    client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)
    imgfile = path
    ori_img = cv2.imread(imgfile)
    height, width, _ = ori_img.shape
    with open(imgfile, 'rb') as fp:
        img_info = fp.read()
    seg_res = client.bodySeg(img_info)
    labelmap = base64.b64decode(seg_res['labelmap'])
    nparr = np.fromstring(labelmap, np.uint8)
    labelimg = cv2.imdecode(nparr, 1)
    labelimg = cv2.resize(labelimg, (width, height), interpolation=cv2.INTER_NEAREST)
    new_img = np.where(labelimg == 1, 255, labelimg)
    result = cv2.bitwise_and(ori_img, new_img)
    cv2.imwrite(path, result)



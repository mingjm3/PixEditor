import cv2 as cv


class Text:

    def addText(self, path, content, fontScale=5, x=0, y=0, color=(255, 255, 255), thickness=1):
        img = cv.imread(path)
        font = cv.FONT_HERSHEY_SIMPLEX
        img = cv.putText(img, content, (x, y), font, fontScale, color, thickness, cv.LINE_AA)
        cv.imwrite(path, img)

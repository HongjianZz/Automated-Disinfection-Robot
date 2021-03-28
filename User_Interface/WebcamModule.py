# import the necessary packages
import time
import cv2

cap = cv2.VideoCapture(0)


def getImg(display=False, size=[480,240]):
    _, img = cap.read()
    img = cv2.resize(img,(size[0],size[1]))
    if display:
        cv2.imshow('cannyEdge',img)
        cv2.waitKey(1)
    return img
def closeImg():
    cap.release()

if __name__ == '__main__':

    while True:
        img = getImg(True)
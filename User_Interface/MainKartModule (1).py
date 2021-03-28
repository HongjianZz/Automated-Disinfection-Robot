from MotorModule import Motor
from LaneDetectionModule import getLaneCurve
import WebcamModule
import cv2

##################################################
motor = Motor(13, 19, 16, 20)
##################################################

def main1():
    img = WebcamModule.getImg()
    curveVal = getLaneCurve(img,1)

    sen = 5 # SENSITIVITY
    maxVAl= 0.35 # MAX SPEED
    if curveVal>maxVAl:curveVal = maxVAl
    if curveVal<-maxVAl: curveVal =-maxVAl
    print(curveVal)
    if curveVal>0:
        if curveVal<0.05: curveVal=0
    else:
        if curveVal>-0.08: curveVal=0
    motor.move(2,curveVal*sen,0.1)
    cv2.waitKey(1)


if __name__ == '__main__':
    while True:
        main1()
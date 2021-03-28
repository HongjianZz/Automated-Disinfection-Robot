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
        sen = 1.7
        if curveVal<0.05: curveVal=0
    else:
        if curveVal>-0.08: curveVal=0
    motor.move(2,curveVal*sen,0.1)
    cv2.waitKey(1)


if __name__ == '__main__':
    while True:
        main1()
        
        
# from MotorModule import Motor
# from LaneDetectionModule import getLaneCurve
# import WebcamModule
# import cv2
# import time
# 
# 
# 
# #################################################
# 
# ##################################################
# 
# def main1():
#     img = WebcamModule.getImg()
#     curveVal = getLaneCurve(img,2)
# 
#     sen = 5 # SENSITIVITY
#     maxVAl= 0.35 # MAX SPEED
#     if curveVal>maxVAl:curveVal = maxVAl
#     if curveVal<-maxVAl: curveVal =-maxVAl
# #     print(curveVal)
#     if curveVal>0:
#         if curveVal<0.05: curveVal=0
#     else:
#         if curveVal>-0.05: curveVal=0
#     print(curveVal)
# #     motor.move(3,curveVal,0.05)
#     motor = Motor(13, 19, 16, 20)
#     motor.move(2,curveVal*sen,0.1)
#     cv2.waitKey(1)
# 
# def mainfile():
#     if __name__ == '__main__':
#         x = time.time()
#         while True:
#             img = WebcamModule.getImg()
#             getLaneCurve(img,2)
#             if x+4 < time.time():4
#             break
#             cv2.waitKey(1)
#         #sleep(1)
#         while True:
#             main1()
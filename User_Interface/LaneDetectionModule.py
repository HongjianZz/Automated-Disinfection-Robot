import cv2
import numpy as np
import os
import utils

dirname = os.path.dirname(__file__) + '/'
curveList = []
avgVal = 7
def getLaneCurve(frame, display=2):
    frameCopy = frame.copy()
    imgResult = frame.copy()
    ### STEP 1
    frameThres = utils.thresholding(frame)

    ### STEP 2
    hT, wT, c = frame.shape

    points = [(128, 159), (wT-100, 80), (16, 240), (wT-20, 200)]
    # USE TO TWEAK THE WARPING -->
    initialTrackBarValues = [124,141,20,240]
    utils.initializeTrackbars(initialTrackBarValues)
    points = utils.valTrackbars()
    frameWarp = utils.warpImg(frameThres, points, wT, hT)
    frameWarpPoints = utils.drawPoints(frameCopy, points)

    ### STEP 3
    midPoint, frameHist = utils.getHistogram(frameWarp, 0.1, 5, display=True)
    curveAveragePoint, frameHist = utils.getHistogram(frameWarp, 0.1, 1, display=True)
    curveRaw = curveAveragePoint - midPoint

    ### STEP 4
    curveList.append(curveRaw)
    if len(curveList) > avgVal: curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))

    ### STEP 5
    if display != 0:
        imgInvWarp = utils.warpImg(frameWarp, points, wT, hT,inv = True)
        imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT//3,0:wT] = 0,0,0
        imgLaneColor = np.zeros_like(frame)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
        midY = 450
        cv2.putText(imgResult,str(curve),(wT//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
        cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(255,0,255),5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                        (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
        # fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        # cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    if display == 2:
        imgStacked = utils.stackImages(0.7,([frame,frameWarpPoints,frameWarp],
                                         [frameHist,imgLaneColor,imgResult]))
        cv2.imshow('ImageStack',imgStacked)
    elif display == 1:
        cv2.imshow('Resutlt',imgResult)

    # Normalisation
    curve = curve / 100
    if curve > 1: curve = 1
    if curve < -1: curve = -1
    return curve


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():  # Check if camera opened successfully
        print("Error opening video stream or file")
    initialTrackBarValues = [100, 80, 20, 100]
    utils.initializeTrackbars(initialTrackBarValues)


    frameCounter = 0
    print('success')
    while cap.isOpened():  # Read until video is completed
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        ret, frame = cap.read()  # Capture frame-by-frame
        if ret:
            frame = cv2.resize(frame, (480, 240))  # RESIZE
            curve = getLaneCurve(frame, display=2)
#             print(curve)
            cv2.imshow('Frame', frame)  # Display the resulting frame
            cv2.waitKey(1) # Optional?
            if cv2.waitKey(25) & 0xFF == ord('q'):  # Press Q on keyboard to exit
                break
        else:  # Break the loop
            break
    cap.release()  # When everything done, release the video capture object
    cv2.destroyAllWindows()  # Closes all the frames
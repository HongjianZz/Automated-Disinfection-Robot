import RPi.GPIO as GPIO
from flask import Flask, render_template, Response, request
from time import sleep
import serial
from MotorModule import Motor
from LaneDetectionModule import getLaneCurve
import WebcamModule
import cv2
import multiprocessing

initi = 0
userValue = 0
kart = 0
i = 0
app = Flask(__name__)



def main1():
    motor = Motor(13,19,16,20)
    while True:
        img = WebcamModule.getImg()
        curveVal = getLaneCurve(img,1)
        sleep(0.01)
        sen = 5 # SENSITIVITY
        maxVAl= 0.35 # MAX SPEED
        if curveVal>maxVAl:curveVal = maxVAl
        if curveVal<-maxVAl: curveVal =-maxVAl
        print('curvel')
        print(curveVal)
        if curveVal>0:
            if curveVal<0.05: curveVal=0
        else:
            if curveVal>-0.08: curveVal=0
        motor.move(2,curveVal*sen,0.1)
        print('motor commend sent')
        cv2.waitKey(1)

process = multiprocessing.Process(target=main1, args=())


@app.route("/", methods=["GET", "POST"])
def home():
    global initi
    global userValue
    global motor
    global kart
    print('/')
    global i
#     motor.stop(0,0,0)
    TES_pin = 26
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TES_pin, GPIO.OUT)
    GPIO.output(TES_pin, GPIO.LOW)
    print("Pump Off")
    initi = 0

    if kart == 1:
        print("trying to stop thread")
        process.terminate()
        sleep(2)
       # process.close()
        i = 0
        motor = Motor(13,19,16,20)
        motor.stop()
        kart = kart -1;

    return render_template("index.html")  # nothing happen

    # To Power on the motor, pump and etc
@app.route('/on', methods=["GET", "POST"])


def on():
    global initi
    global userValue
    global curveVal
    global i 
    global kart
    sen = 5 # SENSITIVITY

    if i == 0:
        process.start()
        kart = 1
        i = i + 1 ;

    if  initi == 0:
        RelayControl = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RelayControl, GPIO.OUT)
        GPIO.output(RelayControl, GPIO.HIGH)
        initi = 1
        print('on1')
        sleep(2)
        return render_template('on.html')

        

    elif request.method == "POST":
        print('Post Request')
        userValue = request.form["val"]  # get the value of val from html file and store as str
        print(userValue)
        SMotor_Control(userValue)
        return render_template('on.html')


    elif request.method == "GET":
        print("Get")
        Data = WaterLevelRead()
        return render_template('on.html',data=Data)
     



def SMotor_Control(degree):
    print("Spray Motor Control")
    val1 = SetAngle(degree)
    servoM1_pin = 6  # PWM pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoM1_pin, GPIO.OUT)
    m1 = GPIO.PWM(servoM1_pin, 50)
    m1.start(0)
    m1.ChangeDutyCycle(12)
    sleep(4)
    m1.ChangeDutyCycle(val1)
    sleep(2)
    #GPIO.cleanup()


def SetAngle(angle):
    angle1 = float(angle)
    print(angle1)
    angle1 += 90
    print(angle1)
    duty = 12 - (angle1 / 180) * 10
    result = int(duty)
    print(duty)
    print(result)
    return result

def WaterLevelRead(): 
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()
    sleep(1)
    Line = ser.readline().decode('utf-8').rstrip()
    print(Line)
    ser.close()
    return Line


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)

    
        


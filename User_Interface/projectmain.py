import RPi.GPIO as GPIO
from flask import Flask, render_template, Response, request
from mycamera import VideoCamera
import time
import serial

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.
initi = 0
userValue = 0
app = Flask(__name__)

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/", methods=["GET", "POST"])
def home():
    global initi
    global userValue
    TES_pin = 26
    if request.method == "POST":
        initi = 0
        userValue = request.form["val"]  # get the value of val from html file and store as str
        print("Please Turn On the Device First")
        return render_template("index.html")  # turn On switch
    else:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TES_pin, GPIO.OUT)
        GPIO.output(TES_pin, GPIO.LOW)
        print("Pump Off")
        initi = 0
        return render_template("index.html")  # nothing happen

    # Spray Power ON


@app.route('/on', methods=["GET", "POST"])
def on():
    global initi
    global userValue
    if  initi == 0:
        RelayControl = 26
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RelayControl, GPIO.OUT)
        GPIO.output(RelayControl, GPIO.HIGH)
        initi = 1
        return render_template('on.html')

    elif request.method == "POST":
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
    GPIO.cleanup()


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
    time.sleep(1)
    Line = ser.readline().decode('utf-8').rstrip()
    print(Line)
    ser.close()
    return Line


if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=False)

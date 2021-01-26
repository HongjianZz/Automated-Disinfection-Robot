from flask import Flask, redirect, url_for, render_template, request
from time import sleep

import RPi.GPIO as GPIO # import the RPi library and its GPIO function?? PWM to control the servo motor??

app = Flask(__name__)

#Default page(Spray Power Off)
@app.route("/", methods=["GET","POST"])
def home():
    TES_pin = 26
    if request.method =="POST":
        print("has posted")
        userValue = request.form["val"] # get the value of val from html file and store as str
        print("Please Turn On the Device First")
        return render_template("index.html") #turn On switch
    else:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TES_pin,GPIO.OUT)
        GPIO.output(TES_pin,GPIO.LOW)
        print("Pump Off")
        return render_template("index.html") # nothing happen

    #Spray Power ON
@app.route('/on',methods=["GET","POST"])
def on():
    RelayControl = 26
    print("Three")
    if request.method =="POST":
        userValue = request.form["val"] # get the value of val from html file and store as str
        print(userValue)
        SMotor_Control(userValue)
        return render_template('on.html')
    else:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RelayControl,GPIO.OUT)
        GPIO.output(RelayControl,GPIO.HIGH)

        return render_template('on.html')



def SMotor_Control(degree):
    print("Spray Motor Control")
    val1=SetAngle(degree)
    servoM1_pin = 6 # PWM pin 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoM1_pin,GPIO.OUT)
    m1=GPIO.PWM(servoM1_pin,50)
    m1.start(0)
    m1.ChangeDutyCycle(12)
    sleep(4)
    m1.ChangeDutyCycle(val1)
    sleep(2)
    GPIO.cleanup()

    

def SetAngle(angle):
    angle1 = float(angle)
    print(angle1)
    angle1+=90
    print(angle1)
    duty = 12-(angle1/180)*10
    result=int(duty)
    print(duty)
    print('Result')
    print(result)
    return result



# initialize the calling
if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 5000)
    






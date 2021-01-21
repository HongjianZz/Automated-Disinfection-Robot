from flask import Flask, redirect, url_for, render_template, request


import RPi.GPIO as GPIO # import the RPi library and its GPIO function?? PWM to control the servo motor??

app = Flask(__name__)

#Default page(Spray Power Off)
@app.route("/", methods=["GET","POST"])
def home():
    TES_pin = 26
    if request.method =="POST":
        userValue = request.form["val"] # get the value of val from html file and store as str
        SpraySwitch = request.form["Chekbox"]
        print(userValue)
        print(SpraySwitch)
        IntVal = int(userValue)
        if SpraySwitch == 0:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(TES_pin,GPIO.OUT)
            print("One")
            GPIO.output(TES_pin,GPIO.LOW)
            return render_template("index.html") # Enable off, turn off the sprayer, no motion
        else:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(TES_pin,GPIO.OUT)
            GPIO.output(TES_pin,GPIO.HIGH)
            print("Two")
            return render_template("on.html") #turn On switch
    else:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TES_pin,GPIO.OUT)
        GPIO.output(TES_pin,GPIO.LOW)
        print("FOUR")
        return render_template("index.html") # nothing happen

    #Spray Power ON
@app.route('/on')
def on():
    RelayControl = 26
    print("Three")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RelayControl,GPIO.OUT)
    GPIO.output(RelayControl,GPIO.HIGH)
    return render_template('on.html')



def Spray_Control(power, readback):
    servoM1_pin = 17 # PWM pin 
    servoM2_pin = 18
    GPIO.setup(servoM1_pin, GPIO.OUT)
    GPIO.setup(servoM2_pin, GPIO.OUT)
    GPIO.cleanup() # clean up other GIPO assignments

    M1 = GPIO.PWM(servoM1_pin, 50)# GPIO 17 for PWM with 50Hz
    M2 = GPIO.PWM(servoM2_pin, 50)# -----18 ---



# initialize the calling
if __name__ == "__main__":
    app.run(host='0.0.0.0',port = 5000)
    






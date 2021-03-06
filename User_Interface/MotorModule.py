import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Motor():
    def __init__(self, En1,En2,En3,En4):
        self.En1 = En1 # right side
        self.En2 = En2 # right side
        self.En3 = En3 # left side
        self.En4 = En4 # left side

        GPIO.setup(self.En1,GPIO.OUT)
        GPIO.setup(self.En2,GPIO.OUT)
        GPIO.setup(self.En3,GPIO.OUT)
        GPIO.setup(self.En4,GPIO.OUT)

        self.pwm1 = GPIO.PWM(self.En1, 100) #100Hz pwm
        self.pwm1.start(50)
        self.pwm2 = GPIO.PWM(self.En2, 100) #100Hz pwm
        self.pwm2.start(50)
        self.pwm3 = GPIO.PWM(self.En3, 100)  # 100Hz pwm
        self.pwm3.start(50)
        self.pwm4 = GPIO.PWM(self.En4, 100)  # 100Hz pwm
        self.pwm4.start(50)
        dutycycle = 13
        self.pwm1.ChangeDutyCycle(dutycycle)
        self.pwm2.ChangeDutyCycle(dutycycle)
        self.pwm3.ChangeDutyCycle(dutycycle)
        self.pwm4.ChangeDutyCycle(dutycycle)
        
    def move(self,speed=2,turn=0,t=0):
        
         leftSpeed = 13 + speed + turn
         rightSpeed = 13 - speed + turn
         
         if leftSpeed>20: leftSpeed=20
         elif leftSpeed<4: leftSpeed= 4
         if rightSpeed>20: rightSpeed=20
         elif rightSpeed<4: rightSpeed= 4
         
         self.pwm3.ChangeDutyCycle(leftSpeed)
         self.pwm1.ChangeDutyCycle(rightSpeed)
         self.pwm4.ChangeDutyCycle(leftSpeed)
         self.pwm2.ChangeDutyCycle(rightSpeed)
         sleep(t)

if __name__ == '__main__':
    motor1 = Motor(13,19,16,20)
    while True:
        motor1.move(2,-2,0)
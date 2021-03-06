#!/usr/bin/env python3
import serial
import time
x = 0
if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.flush()

    while x <20 :
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            time.sleep(1)
            x =x+1

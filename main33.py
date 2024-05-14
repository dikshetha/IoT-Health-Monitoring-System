import time
import numpy as np
import os
import serial
import time
import requests
import math
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)

buzzer = 26
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, GPIO.LOW)

TOKEN = "BBUS-ENjmIby81eg8bBTuDPzEIYhhfnmohZ" # Token
DEVICE_LABEL = "raspidevice"
VL1 = "temperature"
VL2 = "humidity"
VL3 = "heartbeat"
VL4 = "x1"
VL5 = "y1"
VL6 = "z1"

print ("Processing...")

#port = serial.Serial("COM7", baudrate=9600, timeout=1.0)
#port = "/dev/ttyAMA0"
port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1.0)

def build_payload(var_1, var_2, var_3, var_4, var_5, var_6,
                  temp_val, hum_val, hb_val, x1, y1, z1):

    payload = {var_1: temp_val,
               var_2: hum_val,
               var_3: hb_val,
               var_4: x1,
               var_5: y1,
               var_6: z1}             
               
    return payload


def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

def Get_Serial_Data():
    Byte_Range = 1024
    for Idx in range(Byte_Range):
        Serail_Data = port.readline()
        #print(Serail_Data)
        Serail_Data_Decode = Serail_Data.decode('utf-8')
        if len(Serail_Data_Decode) > 5:
            Info_Set = True
            break
    else:
        Byte_Range = Byte_Range + 1
    while Info_Set:
        sensor_value = Serail_Data_Decode.split('*')
        
        temp_val  = sensor_value[0]
        hum_val   = sensor_value[1]
        hb_val    = sensor_value[2]
        x1        = sensor_value[3]
        y1        = sensor_value[4]
        z1        = sensor_value[5].rstrip()

        temp_val  = float(temp_val)
        hum_val   = float(hum_val)
        hb_val    = (float(hb_val) * 100) / 1000
        if hb_val < 55:
            hb_val = 0
        x1        = float(x1)
        y1        = float(y1)
        z1        = float(z1)        
        
        Info_Set = False
        return temp_val, hum_val, hb_val, x1, y1, z1

if __name__ == '__main__':
    while True:
        try:
            temp_val, hum_val, hb_val, x1, y1, z1 = Get_Serial_Data()
            print('Temperature  : ' + str(temp_val)  + ' degC')
            print('Humidity     : ' + str(hum_val) + ' g.m-3')
            print('Heart Beat   : ' + str(hb_val)   + ' bpm')
            print('X1           : ' + str(x1)   + ' X')
            print('Y1           : ' + str(y1)   + ' Y')
            print('Z1           : ' + str(z1)   + ' Z')            
            print('\n')
            time.sleep(1)
            port.flushInput()

            payload = build_payload(
                VL1, VL2, VL3, VL4, VL5, VL6,
                temp_val, hum_val, hb_val, x1, y1, z1)

            print("[INFO] Attemping to send data")
            post_request(payload)
            print("[INFO] finished\n")

            if temp_val > 38 or hb_val > 110:
                GPIO.output(buzzer, GPIO.HIGH)
            else:
                GPIO.output(buzzer, GPIO.LOW)

        except:
            print('Reading Serial')

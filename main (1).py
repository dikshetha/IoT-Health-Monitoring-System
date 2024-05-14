import time
import numpy as np
import os
import serial
import requests
import math
import random
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
buzzer = 26      #26 is pin 
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, GPIO.LOW)

print ("Processing...")

port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=1.0)    #serial communication through usb 
                                                                    #baudrate -> port number 


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
        if hb_val < 40:
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
            sensor_txt_path = r'/var/www/html/sensor_data.txt'
            sensor_f = open(sensor_txt_path, "w")
            sensor_f.write(str(temp_val) + '*' + str(hum_val) + '*' + str(hb_val) + '*' + str(x1) + '*' + str(y1) + '*' + str(z1))
            sensor_f.close()            
            print('Temperature  : ' + str(temp_val)  + ' degC')
            print('Humidity     : ' + str(hum_val) + ' g.m-3')
            print('Heart Beat   : ' + str(hb_val)   + ' bpm')
            print('X1           : ' + str(x1)   + ' X')
            print('Y1           : ' + str(y1)   + ' Y')
            print('Z1           : ' + str(z1)   + ' Z')
            print('\n')
            time.sleep(3)
            port.flushInput()
            if(hb_val>110 or hb_val<50):
                account_sid = 'AC2189c832f54015bd052c0123763fb61f'
                auth_token = 'fa0f4ec7d5de3b41eff07bd83c92e360'
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                from_='+18582958642',
                body='Hello!, check me once...',
                to='+917382225656'
                )

                GPIO.output(buzzer, GPIO.HIGH)
            else:
                GPIO.output(buzzer, GPIO.LOW)

        except:
            print('Reading Serial')

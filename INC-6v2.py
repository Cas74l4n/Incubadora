#import threading
import RPi.GPIO as GPIO
import Adafruit_DHT
import datetime
#import smbus
import time
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
#from multiprocessing import Pool
#import DistanceSensor

SENSOR_DHT1 = Adafruit_DHT.DHT22
#GPIO4
PIN_DHT1 = 4

SENSOR_DHT2 = Adafruit_DHT.DHT22
#GPIO17
PIN_DHT2 = 17

lcd = LCD()
# bus = smbus.SMBus(1)
# time.sleep(1)

#PIN
led_rojo = 36
led_verde = 38
led_azul = 40

#Foco1 33
R_1 = 33

#Foco2 32
R_6 = 32


#Ventilador_Rasp 31
R_2 = 31

#Ventilador_Extractor 29
R_3 = 29

#Ventilador_Disipador
R_4 = 23

#Inc
R_5 = 21

#Sensor Ultrasonico
Echo=37
Trigger=35


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
#LEDS
GPIO.setup(led_verde, GPIO.OUT)
GPIO.output(led_verde, GPIO.LOW)
GPIO.setup(led_azul, GPIO.OUT)
GPIO.output(led_azul, GPIO.LOW)
GPIO.setup(led_rojo, GPIO.OUT)
GPIO.output(led_rojo, GPIO.LOW)

#RELAYS
GPIO.setup(R_1, GPIO.OUT)
#GPIO.output(R_1, GPIO.LOW)
GPIO.setup(R_2, GPIO.OUT)
#GPIO.output(R_2, GPIO.LOW)
GPIO.setup(R_3, GPIO.OUT)
#GPIO.output(R_3, GPIO.HIGH)
GPIO.setup(R_4, GPIO.OUT)
#GPIO.output(R_4, GPIO.HIGH)
GPIO.setup(R_5, GPIO.OUT)
#GPIO.output(R_5, GPIO.LOW)
GPIO.setup(R_6, GPIO.OUT)
#GPIO.output(R_6, GPIO.LOW)



#Sensor
GPIO.setup(Trigger, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

# def bandeja():
#     GPIO.output(R_5, GPIO.HIGH)
#     time.sleep(10)#21600
#     GPIO.output(R_5, GPIO.LOW)
#     time.sleep(5)#120
#     
# bandeja()

# def safe_exit(signum, frame):
#     exit(1)
# 
# signal(SIGTERM, safe_exit)
# signal(SIGHUP, safe_exit)

try:
    while True:
        # Aca se sensa la Temperatura
        #GPIO.cleanup()
        hum1, temp1 = Adafruit_DHT.read(SENSOR_DHT1, PIN_DHT1)
        hum2, temp2 = Adafruit_DHT.read(SENSOR_DHT2, PIN_DHT2)
        
        if hum1 is not None and temp1 is not None:
            print('Temp1={0:0.1f}C Hum1={1:0.1f}%'.format(temp1, hum1))

#            lcd.text(('Temp1={0:0.1f} C Hum1={1:0.1f}%'.format(temp1, hum1)),1) 
#             archivo = open("datos1.txt","a+")
#             archivo.write(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S  ') + str(temp1)+"  " +  str(hum1)+"\n" )
#             archivo.close()
           
            time.sleep(2) #1800
            
            if temp1 < 37.2: #36.6
                #LOW significa encendido/High apagado
                #debe ser al reves
                GPIO.output(led_azul, GPIO.HIGH)
                GPIO.output(led_verde, GPIO.LOW)
                GPIO.output(led_rojo, GPIO.LOW)
                GPIO.output(R_1, GPIO.HIGH)
                GPIO.output(R_3, GPIO.LOW)
                GPIO.output(R_4, GPIO.LOW)
                GPIO.output(R_6, GPIO.HIGH)
                
            elif temp1 > 37.2 and temp1 <= 38.2:
                GPIO.output(led_verde, GPIO.HIGH)
                GPIO.output(led_azul, GPIO.LOW)
                GPIO.output(led_rojo, GPIO.LOW)
                GPIO.output(R_1, GPIO.LOW)
                GPIO.output(R_3, GPIO.LOW)
                GPIO.output(R_4, GPIO.LOW)
                GPIO.output(R_6, GPIO.HIGH)
                
            elif temp1 > 38.2 and temp1 <= 45:
                GPIO.output(led_verde, GPIO.LOW)
                GPIO.output(led_azul, GPIO.LOW)
                GPIO.output(led_rojo, GPIO.HIGH)
                GPIO.output(R_1, GPIO.LOW)
                GPIO.output(R_3, GPIO.HIGH)
                GPIO.output(R_4, GPIO.LOW)
                GPIO.output(R_6, GPIO.LOW)
                
            elif temp1 > 45:
                GPIO.output(led_verde, GPIO.LOW)
                GPIO.output(led_azul, GPIO.LOW)
                GPIO.output(led_rojo, GPIO.HIGH)
                GPIO.output(R_1, GPIO.LOW)
                GPIO.output(R_3, GPIO.HIGH)
                GPIO.output(R_4, GPIO.HIGH)
                GPIO.output(R_6, GPIO.LOW)  
        else:
            print("Falla en la lectura 1")
            time.sleep(2)
        
        GPIO.output(Trigger, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(Trigger, GPIO.LOW)
            
        while GPIO.input(Echo)== False:
            inicio = time.time()
            
        while GPIO.input(Echo) == True:
            fin = time.time()
            
        sig_time = fin-inicio
        distancia = (sig_time * 34300)/2
        
        print("Distancia: %.2f cm" % distancia)
        #time.sleep(2)
            
        if distancia < 35:
            print("Puerta Cerrada")
            lcd.text("Puerta Cerrada",2)
            time.sleep(1)
                
        else:
            print("PUERTA ABIERTA")
            lcd.text("PUERTA ABIERTA",2)
            time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
     lcd.clear()
     GPIO.cleanup()
     #continue
# try:
#     while True:
#         GPIO.output(R_5, GPIO.HIGH)
#         time.sleep(10)#21600
#         GPIO.output(R_5, GPIO.LOW)
#         time.sleep(120)
# #120
# finally:
#     GPIO.cleanup() 
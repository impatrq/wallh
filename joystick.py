from machine import ADC,Pin
import time, usocket, network, _thread
from libreria import analogicRead
#https://www.youtube.com/watch?v=bwG1Ne2ZI4g

def thread1():
  while True:
    led.value(1)            #Set led turn on
    time.sleep(0.5)
    led.value(0)            #Set led turn off
    time.sleep(0.5)

adc0=ADC(Pin(36))               #create ADC object
adc1=ADC(Pin(39))
adc2=ADC(Pin(34))               # Dato proveniente del analogico
adc1.atten(ADC.ATTN_11DB)             # Atenuacion de los analogicos
adc2.atten(ADC.ATTN_11DB)             
led=Pin(2,Pin.OUT)                    # Pin del esp
logic_state2 = 1                      # Stepper Logic State
sta_if = network.WLAN(network.STA_IF) # Network 

if not sta_if.isconnected():
    '''Conexion a internet'''
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('esp','12345678')
    while not sta_if.isconnected():
      pass

sta_if.ifconfig(("192.168.100.207","255.255.255.0","192.168.100.2","8.8.8.8")) # Seteo de ip 
print('network config:', sta_if.ifconfig()[0])

s = usocket.socket()
s.connect(("192.168.100.205",2020))   # Conectar cliente al servidor

_thread.start_new_thread(thread1,())  

while True:
    '''Lectura de pines ADC y envío a traves de socket'''
    analogicRead(adc1, adc2, adc0, s)
    time.sleep(1.0)

    
    
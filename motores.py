from machine import Pin, I2C, UART
import network, time, usocket, _thread
from libreria import HCSR04, Motor, create, Stepper, ultrasonicRead
import max30100
import json

motores = Motor(16, Pin.OUT,17, Pin.OUT,18, Pin.OUT,19, Pin.OUT)
sta_if = network.WLAN(network.STA_IF)
led=Pin(2,Pin.OUT)  
    
sensora1 = HCSR04(trigger_pin=27, echo_pin=26)
sensora2 = HCSR04(trigger_pin=27, echo_pin=10)
sensorb3 = HCSR04(trigger_pin=27, echo_pin=13)
s1 = create(Pin(15,Pin.OUT), Pin(1,Pin.OUT), Pin(0,Pin.OUT), Pin(4,Pin.OUT), delay=2)

def thread1():
  '''Blink'''
  while True:
    led.value(1)            #Set led turn on
    time.sleep(0.5)
    led.value(0)            #Set led turn off
    time.sleep(0.5)

def thread2(sensora1, sensora2, sensorb3):
  
  '''Control de motores con interrupciones de sensor de distancia'''
  (sc,addr) = s.accept()
  print(addr)
  logic_state2 = 1
  continuar2=True
  while continuar2:
    mensaje = sc.recv(64)
    print(str(mensaje[0:12]),"primero")
        
    if str(mensaje[0:14]) == "b'Adelante()'":
      print("Adelante()")
      motores.Adelante()
    
    elif str(mensaje[0:14]) == "b'GirarIzq()'":
      print("GirarIzq()")
      motores.GirarIzq()
    
    elif str(mensaje[0:14]) == "b'GirarDer()'":
      print("GirarDer()")
      motores.GirarDer()
    
    elif str(mensaje[0:16]) == "b'GirarAtras()'":
      print("GirarAtras()")
      motores.Atras()
    
    elif str(mensaje[0:10]) == "b'Boton()'":
      if logic_state2 == 1:
        s1.angle(60)
        logic_state2 += 1 
        print("la sube")
      elif logic_state2 == 2:
        s1.angle(60,-1)
        logic_state2 -= 1 
        print("la baja")
    
    elif str(mensaje[0:7]) == "b'Nada'":
      print("Parar")
      motores.Parar()
      
    distancea1, distancea2, distanceb3 = ultrasonicRead(sensora1, sensora2, sensorb3)

    if distancea1 <= 30 and distancea1 != 0:
      motores.Parar()
      print("Sensor A1 detecto")
    
    elif distancea2 <= 30 and distancea2 != 0:
      motores.Parar()
      print("Sensor A2 detecto")
      
    elif distanceb3 <= 30 and distanceb3 != 0:
      motores.Parar()
      print("Sensor B3 detecto")
      
    time.sleep(0.6)
    sc.close()
  s.close()

def thread3():
  '''Recibir datos de sensores de temperatura y oximetro mediante UART'''
  while True:
    uart = UART(1, 115200, tx=6, rx=7)    
    lectura = uart.read()
    metricas = json.loads(lectura)
    
    temperatura = metricas['temperatura']
    oxigeno = metricas['oxigeno']
    pulso = metricas['pulso']

    print("Temperatura: ",temperatura, " Oxigeno en sangre: ", oxigeno, " Pulso: ", pulso)
    time.sleep(1)
  



if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('esp', '12345678')
    while not sta_if.isconnected():
        pass
        
sta_if.ifconfig(('192.168.100.205','255.255.255.0','192.168.100.2','8.8.8.8'))      
print('network config:', sta_if.ifconfig()[0])

print("Conexion establecida")
s= usocket.socket()
s.bind((sta_if.ifconfig()[0],2020))
print("bindeado")
s.listen(10)

motores.Parar()
print("Server iniciado, esperando conexiones")
_thread.start_new_thread(thread1,())



_thread.start_new_thread(thread3,())
_thread.start_new_thread(thread2,())



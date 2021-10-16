from machine import Pin, I2C
import network, time, usocket, _thread
from libreria import HCSR04, Motor, SensorBase, MLX90614, max30100
import stepper 
 
motores = Motor(16, Pin.OUT,17, Pin.OUT,18, Pin.OUT,19, Pin.OUT)
sta_if = network.WLAN(network.STA_IF)
led=Pin(2,Pin.OUT)  
sensora1 = HCSR04(trigger_pin=27, echo_pin=26)
sensora2 = HCSR04(trigger_pin=12, echo_pin=10)
sensorb3 = HCSR04(trigger_pin=12, echo_pin=13)
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
sensormlx = MLX90614(i2c) 
sensormax = max30100.MAX30100(i2c=i2c)
sensormax.enable_spo2()
s1 = create(Pin(15,Pin.OUT), Pin(2,Pin.OUT), Pin(0,Pin.OUT), Pin(4,Pin.OUT), delay=2)
boton = Pin(23, Pin.IN)

def thread1():
  #Blink
  while True:
    led.value(1)            #Set led turn on
    time.sleep(0.5)
    led.value(0)            #Set led turn off
    time.sleep(0.5)

def thread2():
  #Control de motores
  (sc,addr) = s.accept()
  print(addr)
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
  #Control de ultrasonicos
  distancea1 = round(sensora1.distance_cm())
  distancea2 = round(sensora2.distance_cm())
  distanceb3 = round(sensorb3.distance_cm())
  time.sleep(0.6)

def thread4():
  #control de sensor de temperatura
  while True:
    contador = 0
    momento = round(sensormlx.read_object_temp(),2) +3
    if sensormlx >= 30 and sensormlx <= 40:
      for i in range (30):
        temperaturas.append(round(sensormlx.read_object_temp(),2) +3)
        print(" Temperatura de la persona: ", round(sensormlx.read_object_temp(),2) +3)
        time.sleep(1)
      for i in temperaturas[15:30]:
        if contador == 0:
          contador = contador + 1
          pass
        else:
          temperaturas[0] = temperaturas[0] + i
      temperature = temperaturas[0] / 15
    
      if temperature > 38:
        print("Tenes fiebre y tu temperatura es ", temperature)
      else:
        print("No tenes fiebre y tu temperatura es ", temperature)
    else:
      temperaturas = []

def thread5():
  #Control sensor oximetro
  while True:
    sensormax.read_sensor()
    #print(sensor.ir, sensor.red)
    rawspo2 = sensormax.ir
    rawheartrate = sensormax.red

    spo2 = rawspo2/100
    heartrate = rawheartrate/200
    if spo2 > 100 :
      spo2 = 99.9
    elif spo2 < 93.0 and spo2 > 50.0 :
      spo2 = 93.0
    elif spo2 < 49 :
      spo2 = 0.0
    else :
      spo2 = spo2

    if heartrate > 130 :

      heartrate = 150
    elif heartrate < 65 and heartrate > 50 :
      heartrate = 65.0
    elif heartrate < 49 :
      heartrate = 0.0
    else :
      heartrate = heartrate
      
    #os.system("cls")
    if spo2 > 30:
      print("Oxigeno en sangre: ", spo2,"%         Ritmo Card閾哸co: ", heartrate)
    else: 
      print("Tomando mediciones, porfavor espere.")
  
  


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

logic_state2 = 1

_thread.start_new_thread(thread3,())
_thread.start_new_thread(thread2,())
_thread.start_new_thread(thread4,())
_thread.start_new_thread(thread5,())





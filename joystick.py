
from machine import ADC,Pin
import time, usocket, network, _thread
import json
from letras import *
import st7789

def dibujar(tft, mediciones, rows):
    while True:
        if contador2 >= 6 and logic_state == 1:
            mediciones["t"] = mediciones["t"] + "°c"
            imprimir = [mediciones["t"], mediciones["o"], mediciones["p"]]
            contador = 0
            contador2 = 0
            tft.fill(st7789.BLACK)
            
            for lista in imprimir:
                contador += 1
                x = 0
                for palabra in lista:

                    detectprint(palabra,tft,x,rows[contador])
                    x += 36
                    
        time.sleep(1)

def joystick(client, contador2, logic_state, contador):
    while True:
    
    msg = analogicRead(adc1, adc2, adc0)
    
    client.send(msg.encode(FORMAT))
    
    mediciones = (client.recv(512).decode(FORMAT))
    
    mediciones = json.loads(mediciones)
    
    print(mediciones)
    
    contador2 +=1
    
    if msg == "Boton()":
      if logic_state == 0:
        logic_state += 1 
        print("la sube")
        time.sleep(1)
      elif logic_state == 1:
        logic_state -= 1 
        print("la baja")
        time.sleep(1)
        
        

def analogicRead(adc1, adc2, adc0):
  vry = adc1.read()
  vrx = 4095 - adc2.read()
  sw = adc0.read()

  if vrx > 4050:
    return "GirarAtras()"
  elif vrx < 50:
    return "Adelante()"
  elif vry < 50:
    return "GirarIzq()"
  elif vry > 4050:
    return "GirarDer()" 
  elif sw < 50:
    return "Boton()"
  else:
    return "Nada"

sta_if = network.WLAN(network.STA_IF)
FORMAT = 'utf-8'

adc0=ADC(Pin(36))               #create ADC object
adc1=ADC(Pin(39))
adc2=ADC(Pin(34))               # Dato proveniente del analogico
adc1.atten(ADC.ATTN_11DB)             # Atenuacion de los analogicos
adc2.atten(ADC.ATTN_11DB)
tft = st7789.ST7789(
    SPI(1, baudrate=30000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(19)),
    240,
    240,
    reset=Pin(23, Pin.OUT),
    dc=Pin(22, Pin.OUT)
) # Contructor del display

global logic_state
global contador2
global contador
global imprimir
global mediciones

contador = 0
contador2 = 0
rows = [0,42,136,230]
imprimir = []
logic_state = 0

if not sta_if.isconnected():
    '''Conexion a internet'''
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('esp','12345678')
    while not sta_if.isconnected():
      print("conectando")
      time.sleep(2)
      pass

sta_if.ifconfig(("192.168.0.120","255.255.255.0","192.168.0.2","8.8.8.8"))
#print('network config:', sta_if.ifconfig()[0])

client = usocket.socket()
client.connect(("192.168.0.150",2020))

print("antes del while")
tft.init()
tft.fill(st7789.WHITE)

_thread.start_new_thread(joystick(client, contador2, logic_state,contador), ())
_thread.start_new_thread(dibujar(tft, mediciones, rows), ())
    


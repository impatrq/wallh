
from machine import ADC,Pin
import time, usocket, network, _thread

adc0=ADC(Pin(36))               #create ADC object
adc1=ADC(Pin(39))
adc2=ADC(Pin(34))
dato = ""
adc1.atten(ADC.ATTN_11DB)
adc2.atten(ADC.ATTN_11DB)
led=Pin(2,Pin.OUT)  

def thread1():
  while True:
    led.value(1)            #Set led turn on
    time.sleep(0.5)
    led.value(0)            #Set led turn off
    time.sleep(0.5)

sta_if = network.WLAN(network.STA_IF)

logic_state2 = 1

if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('esp','12345678')
    while not sta_if.isconnected():
      pass

sta_if.ifconfig(("192.168.100.207","255.255.255.0","192.168.100.2","8.8.8.8"))
print('network config:', sta_if.ifconfig()[0])


s = usocket.socket()
s.connect(("192.168.100.205",2020))
print("conectado")

_thread.start_new_thread(thread1,())

while True:
  vry = adc1.read()
  vrx = 4095 - adc2.read()
  sw = adc0.read()

  if vrx > 4050:
    print("GirarAtras()")
    dato = "GirarAtras()"
  elif vrx < 50:
    print("Adelante()")
    dato = "Adelante()"
  elif vry < 50:
    print("GirarIzq()")
    dato = "GirarIzq()"
  elif vry > 4050:
    print("GirarDer()")
    dato = "GirarDer()" 
  elif sw < 50:
    print("Boton apretado")
    dato = "Boton()"
  else:
    print("nada apretado")
    dato = "Nada"
  print("")
  s.send(dato.encode())
  time.sleep(1.3)

    
    








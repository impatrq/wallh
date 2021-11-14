import network, time, usocket, _thread
from libreria import Motor, MLX90614, readOxTemp, ultrasonicRead, HCSR04, create, Stepper
import json, max30100
from machine import Pin, I2C

def start(motores, sensormax, sensormlx, sensora1, sensora2, sensorb3, logic_state, s1):
  server.listen(10)
  print(f"[LISTENING] Server is listening")
  while True:
    conn, addr = server.accept()
    print("aca se para")
    _thread.start_new_thread(handle_client(conn, addr,motores, sensormax, sensormlx, sensora1, sensora2, sensorb3, logic_state, s1))
    print(f"[ACTIVE CONNECTIONS]")
  conn.close()

def handle_client(conn, addr, motores, sensormax, sensormlx, sensora1, sensora2, sensorb3, logic_state, s1):
    print(conn, addr)
    print("[NEW CONNECTION] connected.")

    temperatura, oxigeno, pulso = readOxTemp(sensormax, sensormlx)
    
    mediciones = {
    'temperatura': temperatura,
    'oxigeno': oxigeno,
    'pulso': pulso
    }
    
    while True:
      mensaje = conn.recv(64).decode(FORMAT)

      if ultrasonicRead(sensora1, sensora2, sensorb3) == "Stop": 
        pass
      else:
        if str(mensaje) == 'Adelante()':
          print("Adelante()")
          motores.Adelante()
        
        elif str(mensaje[0:14]) == 'GirarIzq()':
          print("GirarIzq()")
          motores.GirarIzq()
        
        elif str(mensaje[0:14]) == 'GirarDer()':
          print("GirarDer()")
          motores.GirarDer()
        
        elif str(mensaje[0:16]) == 'GirarAtras()':
          print("GirarAtras()")
          motores.Atras()
        
        elif str(mensaje[0:10]) == 'Boton()':
          if logic_state == 1:
            s1.angle(60)
            logic_state += 1 
            print("la sube")
          elif logic_state == 2:
            s1.angle(60,-1)
            logic_state -= 1 
            print("la baja")
        
        elif str(mensaje[0:7]) == 'Nada':
          print("Parar")
          motores.Parar()
       
      temperatura, oxigeno, pulso = readOxTemp(sensormax, sensormlx)
      
      mediciones = {
      'temperatura': temperatura,
      'oxigeno': oxigeno,
      'pulso': pulso
      }

      diccionario = json.dumps(mediciones)

      conn.sendall(diccionario.encode(FORMAT))
      
      time.sleep(1)
    
    conn.close()



FORMAT = 'utf-8'
sta_if = network.WLAN(network.STA_IF)

if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('esp','12345678')
    while not sta_if.isconnected():
        pass
        
sta_if.ifconfig(('192.168.100.215','255.255.255.0','192.168.100.2','8.8.8.8'))      
print('network config:', sta_if.ifconfig()[0])
server= usocket.socket()

time.sleep(2)

server.bind(("192.168.100.215",2020))
print("binded")
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
sensormlx = MLX90614(i2c) 
sensormax = max30100.MAX30100(i2c=i2c)
sensormax.enable_spo2()

motores = Motor(16, Pin.OUT,17, Pin.OUT,18, Pin.OUT,19, Pin.OUT)
sensora1 = HCSR04(trigger_pin=14, echo_pin=27)
sensora2 = HCSR04(trigger_pin=14, echo_pin=26)
sensorb3 = HCSR04(trigger_pin=14, echo_pin=25)
s1 = create(Pin(15,Pin.OUT), Pin(2,Pin.OUT), Pin(0,Pin.OUT), Pin(4,Pin.OUT), delay=2)
logic_state = 0




print("[STARTING] server is starting...")
start(motores, sensormax, sensormlx, sensora1, sensora2, sensorb3, logic_state, s1)

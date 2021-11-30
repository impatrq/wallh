print("[CODE IS STARTING]")
import network, time, usocket, _thread
import json, max30100
from machine import Pin, I2C

try:
    import urequests as requests
except:
    import requests

from libreria import Motor, MLX90614, readOxTemp, create 


def start(motores, sensormax, sensormlx, logic_state, s1):
    logic_state = 1
    server.listen(100)
    print("[LISTENING] Server is listening")
    conna, addra = server.accept()
    print(conna, addra)
    """
    connb, addrb = server.accept()
    print(connb,addrb)
    print("[Ambos Conectados]")"""  
    temperatura, oxigeno, pulso = readOxTemp(sensormax, sensormlx)

    mediciones = {
    'temperatura': temperatura,
    'oxigeno': oxigeno,
    'pulso': pulso
    }


    temperatura, oxigeno, pulso = readOxTemp(sensormax, sensormlx)

    while True:
        try:
            mensajea = conna.recv(64).decode(FORMAT)
                
            if str(mensajea) == 'Adelante()':
              print("Adelante()")
              motores.Adelante()

            elif str(mensajea) == 'GirarIzq()':
              print("GirarIzq()")
              motores.GirarIzq()

            elif str(mensajea) == 'GirarDer()':
              print("GirarDer()")
              motores.GirarDer()

            elif str(mensajea) == 'GirarAtras()':
              print("GirarAtras()")
              motores.Atras()

            elif str(mensajea) == 'Boton()':
              print("ANASHEEE")
              if logic_state == 1:
                s1.angle(60)
                logic_state += 1 
                print("la sube")
              elif logic_state == 2:
                s1.angle(60,-1)
                logic_state -= 1 
                print("la baja")

            elif str(mensajea) == 'Nada':
              print("Parar")
              motores.Parar()
            
            temperatura, oxigeno, pulso = readOxTemp(sensormax, sensormlx)
            
            tabla = {
            't': temperatura,
            'o': oxigeno,
            'p': pulso
            }
            
            tabla = json.dumps(tabla)
            """
            # Esto lo hizo Fabri
            url = "http://192.168.2.71:5000/add/values"
            
            requests.get(url, json=tabla)
            
            HEADER = 16
            
            length = len(tabla)
            msg_length = str(length)
            msg_length += ' ' * (HEADER - int(msg_length))
            
            connb.send(msg_length.encode(FORMAT))
            # Aca termina
            
            connb.send(tabla.encode(FORMAT))"""
            
            t = "T:" + str(temperatura)[0:4]
            o = "O:" + str(oxigeno)[0:4] + "%"
            p = "P:" + str(pulso)[0:4] 
            
            print(temperatura, oxigeno, pulso)
            
            mediciones = {
            't': t,
            'o': o,
            'p': p
            }
            
            diccionario = json.dumps(mediciones)
            print(diccionario)
            conna.send(diccionario.encode(FORMAT))

            print(mensajea)
            time.sleep(1)

        except:
            mensajea = conna.recv(64).decode(FORMAT)
                
            if str(mensajea) == 'Adelante()':
              print("Adelante()")
              motores.Adelante()

            elif str(mensajea) == 'GirarIzq()':
              print("GirarIzq()")
              motores.GirarIzq()

            elif str(mensajea) == 'GirarDer()':
              print("GirarDer()")
              motores.GirarDer()

            elif str(mensajea) == 'GirarAtras()':
              print("GirarAtras()")
              motores.Atras()

            elif str(mensajea) == 'Boton()':
              print("ANASHEEE")
              if logic_state == 1:
                s1.angle(60)
                logic_state += 1 
                print("la sube")
              elif logic_state == 2:
                s1.angle(60,-1)
                logic_state -= 1 
                print("la baja")

            elif str(mensajea) == 'Nada':
              print("Parar")
              motores.Parar()
            
            temperatura, oxigeno, pulso = readOxTemp(sensormax, sensormlx)
            
            tabla = {
            't': temperatura,
            'o': oxigeno,
            'p': pulso
            }
            
            tabla = json.dumps(tabla)
            """
            # Esto lo hizo Fabri
            url = "http://192.168.2.71:5000/add/values"
            
            requests.get(url, json=tabla)
            
            HEADER = 16
            
            length = len(tabla)
            msg_length = str(length)
            msg_length += ' ' * (HEADER - int(msg_length))
            
            connb.send(msg_length.encode(FORMAT))
            # Aca termina
            
            connb.send(tabla.encode(FORMAT))"""
            
            t = "T:" + str(temperatura)[0:4]
            o = "O:" + str(oxigeno)[0:4] + "%"
            p = "P:" + str(pulso)[0:4] 
            
            print(temperatura, oxigeno, pulso)
            
            mediciones = {
            't': t,
            'o': o,
            'p': p
            }
            
            diccionario = json.dumps(mediciones)
            print(diccionario)
            conna.send(diccionario.encode(FORMAT))

            print(mensajea)
            time.sleep(1)




    conn.close()
        
        
        

FORMAT = 'utf-8'
sta_if = network.WLAN(network.STA_IF)

motores = Motor(16, Pin.OUT,17, Pin.OUT,18, Pin.OUT,19, Pin.OUT)

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
sensormlx = MLX90614(i2c) 
sensormax = max30100.MAX30100(i2c=i2c)
sensormax.enable_spo2()


s1 = create(Pin(15,Pin.OUT), Pin(2,Pin.OUT), Pin(0,Pin.OUT), Pin(4,Pin.OUT), delay=2)
global logic_state
logic_state = 1

if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('esp','12345678')
    while not sta_if.isconnected():
    
        pass
        

sta_if.ifconfig(('192.168.0.150','255.255.255.0','192.168.0.2','8.8.8.8'))      
print('network config:', sta_if.ifconfig()[0])
server = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)


server.bind(("192.168.0.150",2020))
print("binded")
time.sleep(1)

print("[STARTING] server is starting...")
start(motores, sensormax, sensormlx, logic_state, s1)


from machine import Pin, I2C, UART
import time, _thread
from libreria import readOxTemp, MLX90614
import max30100, json

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
sensormlx = MLX90614(i2c) 
sensormax = max30100.MAX30100(i2c=i2c)
sensormax.enable_spo2()
uart = UART(1, 115200, tx=6, rx=7)    

while True:
    temperatura, oxigeno, pulso = readOxTemp(sensormax, sensormlx)

    mediciones = {
        'temperatura': temperatura,
        'oxigeno': oxigeno,
        'pulso': pulso
    }

    uart.write(json.dumps(mediciones))

    time.sleep(1)

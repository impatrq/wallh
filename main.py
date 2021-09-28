from machine import Pin, I2C

import network, time, usocket, _thread

class HCSR04:
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500*2*30):
        self.echo_timeout_us = echo_timeout_us
        # Init trigger pin (out)
        self.trigger = Pin(trigger_pin, mode=Pin.OUT, pull=None)
        self.trigger.value(0)
        # Init echo pin (in)
        self.echo = Pin(echo_pin, mode=Pin.IN, pull=None)

    def _send_pulse_and_wait(self):
        self.trigger.value(0) # Stabilize the sensor
        time.sleep_us(5)
        self.trigger.value(1)
        # Send a 10us pulse.
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110: # 110 = ETIMEDOUT
                raise OSError('Out of range')
            raise ex

    def distance_mm(self):
        """
        Get the distance in milimeters without floating point operations.
        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.34320 mm/us that is 1mm each 2.91us
        # pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582 
        mm = pulse_time * 100 // 582
        return mm

    def distance_cm(self):
        """
        Get the distance in centimeters with floating point operations.
        It returns a float

        """
        pulse_time = self._send_pulse_and_wait()

        # To calculate the distance we get the pulse_time and divide it by 2 
        # (the pulse walk the distance twice) and by 29.1 becasue
        # the sound speed on air (343.2 m/s), that It's equivalent to
        # 0.034320 cm/us that is 1cm each 29.1us
        cms = (pulse_time / 2) / 29.1
        return cms

class Motor:
  def __init__(self, pin1, pinout1, pin2, pinout2, pin3, pinout3, pin4, pinout4):
    self.in1 = Pin(pin1, pinout1)
    self.in2 = Pin(pin2, pinout2)
    self.in3 = Pin(pin3, pinout3)
    self.in4 = Pin(pin4, pinout4)
  
  def Adelante(self):
    self.in1.value(1)
    self.in2.value(0)
    self.in3.value(1)
    self.in4.value(0)

  def GirarIzq(self):
    self.Parar()
    time.sleep(1)
    self.in1.value(1)
    self.in2.value(0)
    self.in3.value(0)
    self.in4.value(0)
    time.sleep(10)
    self.Parar()
  
  def GirarDer(self):
    self.Parar()
    time.sleep(1)
    self.in1.value(0)
    self.in2.value(0)
    self.in3.value(1)
    self.in4.value(0)
    time.sleep(10)
    self.Parar()
    
  def GirarAtras(self):
    self.Parar()
    time.sleep(1)
    self.in1.value(0)
    self.in2.value(0)
    self.in3.value(1)
    self.in4.value(0)
    time.sleep(20)
    self.Parar()
    
    
  def Parar(self):
    self.in1.value(0)
    self.in2.value(0)
    self.in3.value(0)
    self.in4.value(0)
  
  def Atras(self):
    self.Parar()
    time.sleep(1)
    self.in1.value(0)
    self.in2.value(1)
    self.in3.value(0)
    self.in4.value(1)
    time.sleep(3)
    self.Parar()

class SensorBase:
  

	def read16(self, register):
		data = self.i2c.readfrom_mem(self.address, register, 2)
		return ustruct.unpack('<H', data)[0]

	def read_temp(self, register):
		temp = self.read16(register);
		# apply measurement resolution (0.02 degrees per LSB)
		temp *= .02;
		# Kelvin to Celcius
		temp -= 273.15;
		return temp;

	def read_ambient_temp(self):
		return self.read_temp(self._REGISTER_TA)

	def read_object_temp(self):
		return self.read_temp(self._REGISTER_TOBJ1)

	def read_object2_temp(self):
		if self.dual_zone:
			return self.read_temp(self._REGISTER_TOBJ2)
		else:
			raise RuntimeError("Device only has one thermopile")

	@property
	def ambient_temp(self):
		return self.read_ambient_temp()

	@property
	def object_temp(self):
		return self.read_object_temp()

	@property

	def object2_temp(self):
		return self.read_object2_temp()

class MLX90614(SensorBase):
  
	_REGISTER_TA = 0x06
	_REGISTER_TOBJ1 = 0x07
	_REGISTER_TOBJ2 = 0x08

	def __init__(self, i2c, address=0x5a):
		self.i2c = i2c
		self.address = address
		_config1 = i2c.readfrom_mem(address, 0x25, 2)
		_dz = ustruct.unpack('<H', _config1)[0] & (1<<6)
		self.dual_zone = True if _dz else False


def wifi():
  sta_if = network.WLAN(network.STA_IF)
  if not sta_if.isconnected():
      print('connecting to network...')
      sta_if.active(True)
      sta_if.connect('Avionica-2', 'iMpa2020')
      while not sta_if.isconnected():
          pass
  print('network config:', sta_if.ifconfig()[0])

  s= usocket.socket()
  s.bind(("192.168.2.38",2020))
  s.listen(10)


  print("Server iniciado, esperando conexiones")

def thread1():
  #control de movimiento
  motores.Parar()
  continuar1 = True
  while continuar1:
      (sc,addr) = s.accept()
      print(addr)
      continuar2=True
      while continuar2:
          mensaje = sc.recv(64)
          print(str(mensaje[0:12]),"primero")
          if not mensaje:
              continuar2 = False
              
          elif str(mensaje[0:14]) == "b'Adelante()'":
            print("Adelante()")
            motores.Parar()
          
          elif str(mensaje[0:14]) == "b'GirarIzq()'":
            print("GirarIzq()")
            motores.GirarIzq()
          
          elif str(mensaje[0:14]) == "b'GirarDer()'":
            print("GirarDer()")
            motores.GirarDer()
          
          elif str(mensaje[0:16]) == "b'GirarAtras()'":
            print("GirarAtras()")
            motores.GirarAtras()
          
          elif mensaje == "fin":
              continuar1 = False
              print(mensaje.decode())
          sc.close()
      s.close()

def thread2():
  #control de ultrasonicos
  distancias = []
  while True:
    distancias[0] = round(sensora1.distance_cm())
    distancias[1] = round(sensora2.distance_cm())
    distancias[2] = round(sensorb3.distance_cm())
    time.sleep(1.5)

def thread3():
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
  
  
  
#Declaracion de pines de motores
motores = Motor(16, Pin.OUT,17, Pin.OUT,18, Pin.OUT,19, Pin.OUT)
#Declaracion de pines ultrasonicos
sensora1 = hcsr04.HCSR04(trigger_pin=27, echo_pin=26)
sensora2 = hcsr04.HCSR04(trigger_pin=12, echo_pin=10)
sensorb3 = hcsr04.HCSR04(trigger_pin=12, echo_pin=13)
#Declaracion de pines de sensor de temperatura 
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
sensormlx = MLX90614(i2c) 
#Establecer conexion wifi 
wifi()
#Arranque de los hilos
_thread.start_new_thread(thread1,())
_thread.start_new_thread(thread2,())
_thread.start_new_thread(thread3,())





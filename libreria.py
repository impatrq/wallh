from machine import Pin, I2C
import time

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
    self.in1.value(0)
    self.in2.value(1)
    self.in3.value(0)
    self.in4.value(1)

  def GirarIzq(self):
    self.in1.value(1)
    self.in2.value(0)
    self.in3.value(0)
    self.in4.value(1)

  
  def GirarDer(self):
    self.in1.value(0)
    self.in2.value(1)
    self.in3.value(1)
    self.in4.value(0)

    
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
    self.in1.value(1)
    self.in2.value(0)
    self.in3.value(1)
    self.in4.value(0)

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
class Stepper:
    FULL_ROTATION = int(4075.7728395061727 / 8) # http://www.jangeox.be/2013/10/stepper-motor-28byj-48_25.html

    HALF_STEP = [
        [0, 0, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [1, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 1],
    ]

    FULL_STEP = [
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 0, 1]
    ]
    def __init__(self, mode, pin1, pin2, pin3, pin4, delay):
    	if mode=='FULL_STEP':
        	self.mode = self.FULL_STEP
        else:
        	self.mode = self.HALF_STEP
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        self.delay = delay  # Recommend 10+ for FULL_STEP, 1 is OK for HALF_STEP
        
        # Initialize all to 0
        self.reset()
        
    def step(self, count, direction=1):
        """Rotate count steps. direction = -1 means backwards"""
        if count<0:
            direction = -1
            count = -count
        for x in range(count):
            for bit in self.mode[::direction]:
                self.pin1(bit[0])
                self.pin2(bit[1])
                self.pin3(bit[2])
                self.pin4(bit[3])
                time.sleep_ms(self.delay)
        self.reset()
    def angle(self, r, direction=1):
    	self.step(int(self.FULL_ROTATION * r / 360), direction)
    def reset(self):
        # Reset to 0, no holding, these are geared, you can't move them
        self.pin1(0) 
        self.pin2(0) 
        self.pin3(0) 
        self.pin4(0)

def create(pin1, pin2, pin3, pin4, delay=2, mode='HALF_STEP'):
	return Stepper(mode, pin1, pin2, pin3, pin4, delay)

def analogicRead(adc1, adc2, adc0, s):
  vry = adc1.read()
  vrx = 4095 - adc2.read()
  sw = adc0.read()
  dato = ""
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

def ultrasonicRead(sensora1, sensora2, sensorb3):
  distancea1 = round(sensora1.distance_cm())
  distancea2 = round(sensora2.distance_cm())
  distanceb3 = round(sensorb3.distance_cm())
  return(distancea1, distancea2, distanceb3)


def readOxTemp(sensormax, sensor):
    sensormax.read_sensor()
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
    else:
        spo2 = spo2

    if heartrate > 130 :
        heartrate = 150
    elif heartrate < 65 and heartrate > 50 :
        heartrate = 65.0
    elif heartrate < 49 :
        heartrate = 0.0
    else :
        heartrate = heartrate

    temp = round(sensor.read_object_temp(),2)+2

    return temp, spo2, heartrate



import ustruct, time, network
from machine import I2C, Pin

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

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=100000)
sensor = MLX90614(i2c) 
temperaturas = [] 

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect("Fibertel WiFi411 5.8GHz", "0141847689")
station.isconnected()
station.ifconfig()

print(sensor)
for i in range (15):
  temperaturas.append(round(sensor.read_object_temp(),2) +3)
  print(" Temperatura de la persona: ", round(sensor.read_object_temp(),2) +3  , "°C" )
  time.sleep_ms(1000)

contador = 0

for i in temperaturas:
  if contador == 0:
    contador = contador + 1
    pass
  else:
    temperaturas[0] = temperaturas[0] + i


temperature = temperaturas[0] / 15
  
if temperature > 38:
   print("Voce tein feibre y tu temperatura es ", temperature, "°C")
else:
   print("voce tai bien y tu temperatura es ", temperature, "°C")


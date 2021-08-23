
import machine, time
from machine import Pin
import hcsr04


sensor = hcsr04.HCSR04(trigger_pin=13, echo_pin=12)
#sensor1 = hcsr04.HCSR04(trigger_pin=26, echo_pin=27)


while True:
 
  distance = sensor.distance_cm()
  distance = round(distance)

  print('Distance:', distance  , 'cm')
  time.sleep(1)



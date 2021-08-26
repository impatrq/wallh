
from lib.MAX30102 import MAX30102
from machine import sleep
from utime import ticks_diff, ticks_ms
import logging


logging.basicConfig(level=logging.INFO)

# Sensor instance. If left empty, loads default ESP32 I2C configuration
sensor = MAX30102()


# The default sensor configuration is:
# Led mode: 2 (RED + IR)
# ADC range: 16384
# Sample rate: 400 Hz
# Led power: maximum (50.0mA - Presence detection of ~12 inch)
# Averaged samples: 8
# pulse width: 411
print("Setting up sensor with default configuration.", '\n')
sensor.setup_sensor()

sleep(1)

# The readTemperature() method allows to extract the die temperature in °C    
# print("Reading temperature in °C.", '\n')
# print(sensor.readTemperature())

# Select wether to compute the acquisition frequency or not
compute_frequency = False

print("Starting data acquisition from RED & IR registers...", '\n')
sleep(1)

t_start = ticks_ms()    # Starting time of the acquisition
samples_n = 0           # Number of samples that has been collected

while(True):
    # The check() method has to be continuously polled, to check if
    # there are new readings into the sensor's FIFO queue. When new
    # readings are available, this function will put them into the storage.
    sensor.check()
    
    # Check if the storage contains available samples
    if(sensor.available()):
        # Access the storage FIFO and gather the readings (integers)
        red_reading = sensor.popRedFromStorage()
        IR_reading = sensor.popIRFromStorage()
        
        # Print the acquired data (can be plot with Arduino Serial Plotter)
        print(red_reading, ",", IR_reading)
        
        # We can compute the real frequency at which we receive data
        if (compute_frequency):
            samples_n=samples_n+1
            if ( ticks_diff(ticks_ms(), t_start) > 999 ):
                f_HZ = samples_n/1
                samples_n = 0
                t_start = ticks_ms()
                print("acquisition frequency = ",f_HZ)
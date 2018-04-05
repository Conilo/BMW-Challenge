import sys
sys.path.append("/home/pi/bmw/libs")

import time as tm
import distancebk as distance
import powerbk as power
import colorbk as color

# Creates sensor objects
ultrasonic_sensor = distance.distancebk(3)
power_sensor = power.powerbk()
left_color_sensor = color.colorbk(1)
right_color_sensor = color.colorbk(2)

def read_ultrasonic():
    tm.sleep(0.01)
    return ultrasonic_sensor.read()

def read_battery_voltage():
    return power_sensor.readvoltage()

def read_drained_current():
    return power_sensor.readcurrent()

def read_color_values():
    return(right_color_sensor.read("white2"),
           left_color_sensor.read("white2"))

def read_color_strings():
    return(right_color_sensor.read(),
           left_color_sensor.read())

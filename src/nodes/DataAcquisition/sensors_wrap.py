import sys
sys.path.append("/home/pi/bmw/libs")

import time as tm
import distancebk as distance
import powerbk as power
import colorbk as color

# Creates sensor objects
ultrasonic_sensor = distance.distancebk(3)
power_sensor = power.powerbk()
left_color_sensor = color.colorbk(2)
right_color_sensor = color.colorbk(1)

def read_ultrasonic():
    """
    Reads the ultrasonic sensor using 
    bmw provided libs.
    """
    return ultrasonic_sensor.read()

def read_battery_voltage():
    """
    Reads the power sensor voltage value 
    using bmw provided libs.
    """
    return power_sensor.readvoltage()

def read_drained_current():
    """
    Reads the power sensor current value 
    using bmw privided libs.
    """
    return power_sensor.readcurrent()

def read_color_values():
    """
    Reads the light sensor strings using 
    bmw privided libs.
    """
    return(right_color_sensor.read("white"),
           left_color_sensor.read("white"))

def read_color_strings():
    """
    Reads the light sensor values using 
    bmw privided libs.
    """
    return(right_color_sensor.read(),
           left_color_sensor.read())

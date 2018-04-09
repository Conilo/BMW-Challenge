#!/usr/bin/env python
import rospy
import time as tm
from bmw.msg import Sensors
from master_module import Master, \
                          Task, \
                          bw

# Initialices master object
master = Master()

def start_mapping():
    """
    Function that sets the mapping flag
    to start mapping.
    """
    master.mapping_flag = True

def my_shutdown():
    """
    Functions that shutsdown motors
    and clean GPIOs.
    """
    bw.shutdown()

# Iterrupt object declaration
bw.board.Enable_Interrupt_Button(1, start_mapping)

def on_new_sensors_msg(data):
    """
    Function that saves the sensor's data into
    the master object.
    """
    master.distance = data.distance
    master.voltage = data.voltage
    master.current = data.current
    master.left_sensor_value = data.color_values[0]
    master.right_sensor_value = data.color_values[1]

    # Runs the task assigner and solver
    master.run()

def main():

    rospy.init_node('Master')

    rospy.Subscriber(
        '/sensors_data',
        Sensors,
        on_new_sensors_msg,
        queue_size = 1)

    rospy.on_shutdown(my_shutdown)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except:
        bw.shutdown()

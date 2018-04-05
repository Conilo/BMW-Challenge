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
    master.mapping_flag = True
    tm.sleep(0.2)

def my_shutdown():
    bw.shutdown()

bw.board.Enable_Interrupt_Button(1, start_mapping)

# Global parameters

def on_new_sensors_msg(data):
    master.distance = data.distance
    master.voltage = data.voltage
    master.current = data.current
    master.left_sensor_value = data.color_values[0]
    master.right_sensor_value = data.color_values[1]
    master.left_sensor_string = data.color_strings[0]
    master.right_sensor_string = data.color_strings[1]

    master.run()

def main():

    rospy.init_node('Master')

    rospy.Subscriber(
        '/sensors_data',
        Sensors,
        on_new_sensors_msg)

    rospy.on_shutdown(my_shutdown)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except:
        bw.shutdown()

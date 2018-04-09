#!/usr/bin/python
import rospy
import sensors_wrap as sw
import numpy as np
from bmw.msg import Sensors
 
# Global parameters
RATE = 20

# Function that collects data from sensors
def read_sensors():

    # Topic to publish sensor's data
    sensors_pub = \
        rospy.Publisher(
            '/sensors_data',
            Sensors,
            queue_size = 1)
	
    # Creates an msg object of Sensors type.
    msg = Sensors()

    rospy.init_node('DataAcquisition')
    rate = rospy.Rate(RATE)

    while not rospy.is_shutdown():

        # Reads sensors
        color_values_read = int(sw.read_color_values())
        distance_read =  int(sw.read_ultrasonic())
        voltage_read = int(sw.read_battery_voltage())
        current_read = int(sw.read_drained_current())
        color_strings_read = sw.read_color_strings()

	# Verify data to be sent
        if type(distance_read) is int:
	    msg.distance = distance_read
        if type(voltage_read) is int:
            msg.voltage = voltage_read
        if type(current_read) is int:
	    msg.current = current_read
        types = [type(i) is int for i in color_values_read]
        if all(types):
	    msg.color_values = color_values_read

	# Publishes message
        sensors_pub.publish(msg)

	# Spin
        rate.sleep()

if __name__ == '__main__':
    try:
        read_sensors()
    except rospy.ROSInterruptException:
        pass

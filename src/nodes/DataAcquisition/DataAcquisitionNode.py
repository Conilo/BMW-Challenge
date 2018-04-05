#!/usr/bin/python
import rospy
import sensors_wrap as sw
import numpy as np
from bmw.msg import Sensors
 
# Global parameters
RATE = 20

def read_sensors():

    sensors_pub = \
        rospy.Publisher(
            '/sensors_data',
            Sensors,
            queue_size = 1)

    msg = Sensors()

    rospy.init_node('DataAcquisition')
    rate = rospy.Rate(RATE)

    while not rospy.is_shutdown():

        # Gets sensors data
        color_values_read = sw.read_color_values()
        #distance_read =  sw.read_ultrasonic()
        distance_read = int(np.random.normal(50, 10))
        voltage_read = int(sw.read_battery_voltage())
        current_read = int(sw.read_drained_current())
        color_strings_read = sw.read_color_strings()

	# Verify received data
        if type(distance_read) is int:
	    msg.distance = distance_read
        if type(voltage_read) is int:
            msg.voltage = voltage_read
        if type(current_read) is int:
	    msg.current = current_read
        types = [type(i) is int for i in color_values_read]
        if all(types):
	    msg.color_values = color_values_read
        msg.color_strings = color_strings_read

	# Publish message
        sensors_pub.publish(msg)

	# Spin
        rate.sleep()

if __name__ == '__main__':
    try:
        read_sensors()
    except rospy.ROSInterruptException:
        pass

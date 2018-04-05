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
        distance_read =  sw.read_ultrasonic()
        #distance_read = np.random.normal(50, 10)
        voltage_read = sw.read_battery_voltage()
        current_read = sw.read_drained_current()
        color_values_read = sw.read_color_values()
        color_strings_read = sw.read_color_strings()

	# Verify received data
        if (distance_read != 'error'):
	    msg.distance = distance_read
        if (voltage_read != 'error'):
            msg.voltage = voltage_read
        if (current_read != 'error'):
	    msg.current = current_read

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

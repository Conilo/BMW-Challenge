#!/usr/bin/env python
import rospy
import bluetooth as bt
import os
from bmw.msg import Sensors

# Dictionary with the known MAC Addresses
MAC = {'48:3C:0C:9C:AE:02': 'Conilo',
       '5C:51:81:11:7F:F0': 'Pariente',
       '5C:51:88:50:F5:52': 'San Java',
       'D4:A1:48:75:BA:9A': 'Alex'}

# Open server socket on RFCOMM
server_socket = bt.BluetoothSocket(bt.RFCOMM)

# Set server socket parameters
port = 1
server_socket.bind(("", port))
server_socket.listen(1)

# Send each new data message by bluetooth
def on_new_sensors_msg(data):
    """
    This fucntion sends every new data package 
    received to the bluetooth comm port.
    """
    global client_socket
       
    try:
       
        # Waits for the app request 
        receivedData = client_socket.recv(1024)
       
        # Concatenate data to be sent
        sensors_data = \
            " " + "D=" + str(data.distance) + "+" \
            + "V=" + str(data.voltage) + "+" \
            + "C=" + str(data.current) + "+" \
            + "CR=" + str(data.color_values[0]) + "+" \
            + "CL=" + str(data.color_values[1]) + ";\r\n"

        # Send data
        client_socket.send(sensors_data)

    except:
        os.system("rosnode kill BluetoothComm")


def main():

    global client_socket

    rospy.init_node('BluetoothComm')

    # Establishes connection to the ext. device.
    print("Waitting for connection...")
    client_socket, address = server_socket.accept()
    print(" Accepted connection from: " + MAC[address[0]])

    # Subscribes to the sensor's data topic.
    rospy.Subscriber(
        '/sensors_data',
        Sensors,
        on_new_sensors_msg,
        queue_size = 10)

    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except:
        os.system("rosnode kill BluetoothComm")

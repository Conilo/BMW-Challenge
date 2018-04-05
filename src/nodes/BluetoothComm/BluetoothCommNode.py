#!/usr/bin/env python
import rospy
import bluetooth as bt
import os
from bmw.msg import Sensors

# MAC Addresses
MAC = {'48:3C:0C:9C:AE:02': 'Conilo',
       '5C:51:81:11:7F:F0': 'Pariente',
       '5C:51:88:50:F5:52': 'San Java',
       'D4:A1:48:75:BA:9A': 'Alex'}

# Open server socket on RFCOMM
server_socket = bt.BluetoothSocket(bt.RFCOMM)

# Server socket parameters
port = 1
server_socket.bind(("", port))
server_socket.listen(1)

def on_new_sensors_msg(data):

    global client_socket

    # Get some data
    try:
        print("Waitting request...")
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
        print("   Data sent: %s" % sensors_data)

    except:
        os.system("rosnode kill BluetoothComm")


def main():

    global client_socket

    rospy.init_node('BluetoothComm')

    print("Waitting for connection...")
    client_socket, address = server_socket.accept()
    print(" Accepted connection from: " + MAC[address[0]])

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

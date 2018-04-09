# BMW ROS
This is the ROS Repository for the BMW challenge. In this document youl'll find each node and wrapper function inside the system:
- Data acquisition node.
- Bluetooth communication node.
- Master node.

## DataAcquisition node
This node takes care of the sensors data reading and publication. The sampling rate is approximately 20 Hz and it uses a funtions wrap of the bmw libs to read the sensors. The informations is published on the /sensors_data topic.

## BluetoothComm node
This node establishes the communication between the app and the vehicle. It takes the data being published on the sensors topic and send it through bluetooth at 115000 bps.

## Master node
This node takes care of the whole system behaviour, which is based on the car's system status (data aquired from sensors and current position on the map) and executes instructions (motor movements) accordingly. 
There are three main system states:

1. Idle: this state only waits for the "mapping button" or the "escaping button" to be pressed; the second button depens on an existing trajectory (mapping was already run sucessfully).

2. Mapping: this state takes care of the mapping task, in this task the system calculates a exploration trajectory based on the BDS algorith. On each intersection detected, the car looks for gates and colors. Once all the gates have been found, or all intersections visited, the car returns to it origin position and is ready for the escaping task.

3. Escaping: this state takes care of the escaping task in which the car has to drive from the origin position to the end position crossing all gates in order. This trajectory is calculated after the mapping is done an the escape buttton pressed.

## Libraries
This section describes the wraps and libraries implemented for the nodes: eg. the trajectory calculation algorithm.

### Trajectory calculation

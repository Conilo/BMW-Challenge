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

# Trajectory and mapping
This section is about the algorithms that have been used to obtain the desired path
to follow. Also, here is shown our methodology to achieve a correct mapping in few steps.
## BFS
Breadth-first search is an algorithm for traversing or searching tree or graph data structures.
It starts at the tree root (or some arbitrary node of a graph, sometimes referred to as a 'search key) and explores the neighbour nodes first, before moving to the next level neighbours.
```
Wkikipedia https://en.wikipedia.org/wiki/Breadth-first_search
```
We have used BFS to simple determinate the shortest path from a point to a goal. We have used BFS in the next order:

```
Start to Red box
Red box to Green box
Green box to Blue box
Blue box to Yellow box
Yellow box to the End (opposite corner)
```
## Mapping simulation
The idea to do the mapping is to visit every node of the graph just once. This can be done by following a ZigZag path.
![zig](https://user-images.githubusercontent.com/33235648/38570458-8750038c-3cb3-11e8-8520-e1843d931ea7.png)

The image above represents the desired path in case that none box is present, however this will not be the case.
So, to find the boxes and obtain the relevant information, the next senosrs are consider.
1. Color sensor to know the color of the box and to know the current position by counting the nodes.
2. Ultrasonic sensor to know if a box is in vertical position.

So, the idea is to read both sensors in every node, by asking to the sensor color if the reading is different
to black and white. And askig to the ultrasonic if there is any box in front. In case there's a box in front,
we use BFS to determine the path to achieve the node of the box.

The nex image represent a simulation of our methodology to the the mapping.
![sim_map](https://user-images.githubusercontent.com/33235648/38571003-e45fef6e-3cb4-11e8-8ff3-b25f94451904.png)

Also we get the simulation of the sensors. We get the information in every node.
```
(4, 1) blue bellow
(2, 2) There is something in front
(2, 2) yellow bellow
(4, 4) red bellow
(1, 5) There is something in front
(1, 5) green bellow
```
To see this simulation, run the code "mapping_sim.py".

## Path following simulation
Firstly we must create a grid with all its nodes interconnected, this step we call it the graph creation.
In the code "car_movements.py", we can change the size of the grid in te section "number of tiles".
Then we have to update the graph with all the founded boxes so that we can delete the forbidden connections.
This step should be done by the mapping.
Forbbiden connection are the ones which the car cannot traverse.
As in the image bellow.
![con2](https://user-images.githubusercontent.com/33235648/38569088-048f8862-3cb0-11e8-96df-dea6e9e9acfc.png)

Once the graph has been updated, the next step is to determine the shortest path in the order we described above.
Then we determine the angles that the car should turn in every node.
The output is the next:
```
[90, 0, 0, 0, -90, 0, 0, 0, 0, 180, 0, 0, 0, -90, 0, -90, 0, -90, 0, 0, 0, 0, 90, 0, 180, 0, 0, -90, 0, 0, 0, 0, -90, 0, 0, 0]
```
In the next image we see the simulation of the car taversing all the boxes in the specific order. Strating
at the left-down corner  and finishing at the right-upper corner.

![final_path](https://user-images.githubusercontent.com/33235648/38567638-5db27426-3cac-11e8-99fb-dd45342dc3fb.png)

To see this simulation, run the code "car_movements.py".


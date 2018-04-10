from math import *
import robot_model as rb
import mappingBMW as mbmw
from matplotlib import pyplot as plt
import matplotlib.patches as patches

'''This code simulates the car movements, once
it has finished the mapping'''

def angle_correction(angle):
	'''This functions transform angles to the space
	[-pi/2;pi/2] or [-90;90]'''
	x={0:0,90:90,360:0,-360:0,270:-90,-270:90,-90:-90,180:180,-180:180}
	return x[angle]

#Boxes Simulation
#Here the boxes are initialized
#The boxes needs color, orientation, x_coordinate, y coordinate
roja=mbmw.Caja('red','h',4,4)
azul=mbmw.Caja('blue','h',4,1)
verde=mbmw.Caja('green','v',1,5)
amarilla=mbmw.Caja('yellow','v',2,2)
#Boxes junction in the order we want to follow
cajas=[roja,verde,azul,amarilla]
#Boxes plot
rectangles=[i.rect() for i in cajas]
amarilla.plot_caja(rectangles)

#Car simulation
#Initial conditions
bmw=rb.Unicycle()
bmw.pos_x=0
bmw.pos_y=0
bmw.angle=0
bmw.plot = True             # plot the robot!
bmw.plot_robot()
bmw.update()

#Number of tiles of the map
x=7
y=7

#Creation of the grid
grid=mbmw.mappingBMW(x,y)

#Creation of a graph that connects all the neighbours
graph=grid.mapa()
#ZigZag path
s_path=grid.sPath()

#Merge the graph with the boxes
#This must be done by the mapping
#Here the adjacent graph's connections to the boxes are deleted
for i in cajas:
	grid.update_graph(i.get_coordinates(),i.get_orientation()) 

#Path Generation
#Find the shortest in go to goal mode
path=[]
inicio=(0,0)
fin=(x-1,y-1)

#Set the coordinates in the way we want to follow the boxes
uno=[inicio,roja.get_coordinates()]
dos=[roja.get_coordinates(),verde.get_coordinates()]
tres=[verde.get_coordinates(),azul.get_coordinates()]
cuatro=[azul.get_coordinates(),amarilla.get_coordinates()]
cinco=[amarilla.get_coordinates(),fin]

#Find the shortest path to achieve the goal
orden2=[uno,dos,tres,cuatro,cinco]
last=[(),()]
for i in orden2:
	path_short=(mbmw.shortest_path(graph,i[0] ,i[1] )[1:])
	#This code is made to traverse the boxes
	if last[0]==path_short[0]:
		if last[1][1]==path_short[0][1]:
			if last[1][0]>path_short[0][0]:
				coordinate=(last[1][0]+1,last[1][1])
			else:
				coordinate=(last[1][0]-1,last[1][1])
			i.pop(0)
			i.insert(0,coordinate)
			path.append(coordinate)
			path_short=(mbmw.shortest_path(graph,i[0] ,i[1] )[1:])
		elif last[1][0]==path_short[0][0]:
			if last[1][1]>path_short[0][1]:
				coordinate=(last[1][0],last[1][1]+1)
			else:
				coordinate=(last[1][0],last[1][1]-1)
			i.pop(0)
			i.insert(0,coordinate)
			path.append(coordinate)
			path_short=(mbmw.shortest_path(graph,i[0] ,i[1] )[1:])
			print path_short
	last = path_short[-2:]
	path+=path_short


#Get the steering, this is the only parameter that needs the car
comandos=[]
#To solve the problem of float type
delta=0.001

def generate_angles():
	'''It returns a list of commands/angles to follow'''
	for point in range(len(path)):
		ex=path[point][0]-bmw.pos_x
		ey=path[point][1]-bmw.pos_y
		eth=atan2(ey,ex)-bmw.angle
		degrees=eth*180/pi
		#Control output:
		if degrees>0:
			degrees=int(degrees+delta)
		elif degrees<0:
			degrees=int(degrees-delta)


		bmw.vel=0
		bmw.vel_an=eth
		bmw.update()
		bmw.vel_an=0
		bmw.vel=1
		bmw.update()

		comandos.append(angle_correction(degrees))
		bmw.plot_robot()
	return comandos

#Obtain the steering list to follow
steering=generate_angles()
print steering
plt.xlim([-1,x])
plt.ylim([-1,y])

plt.show()
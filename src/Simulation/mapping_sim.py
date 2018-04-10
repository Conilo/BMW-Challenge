from math import *
import robot_model as rb
import mappingBMW as mbmw
from matplotlib import pyplot as plt
import matplotlib.patches as patches

def angle_correction(angle):
	x={0:0,90:90,360:0,-360:0,270:-90,-270:90,-90:-90}
	return x[angle]

#Simulacion cajas
roja=mbmw.Caja('red','h',4,4)
azul=mbmw.Caja('blue','h',4,1)
verde=mbmw.Caja('green','v',1,5)
amarilla=mbmw.Caja('yellow','v',2,2)
#Boxes junction
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

#Number of tiles
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

coordinates=[i.get_coordinates()[:-1] for i in cajas]
print coordinates[0]

def short_mapping(graph,s_path):
	path=[]
	for i in range(len(s_path)-1):
		path_short=shortest_path(graph,s_path[i],s_path[i+1])[1:]
		path+=path_short
	return path

def ter_k(graph,s_path,cajas):
	#Pregunto por abajo
	for i in range(len(s_path)-1):
		#Read Color
		for j in cajas:
			if j.get_caja(s_path[i][0],s_path[i][1])!= None:
				print j.get_coordinates(),j.get_color(),'bellow'
			if j.get_caja(s_path[i+1][0],s_path[i+1][1])!= None:
				if j.get_orientation()=='v':
					grid.update_graph(j.get_coordinates(),j.get_orientation())
					print j.get_coordinates(),'There is something in front'

print graph[1,2]
print len(graph)
ter_k(graph,s_path, cajas)

print s_path[0]
#Path Generation
path=mbmw.short_mapping(graph,s_path)

#Get the steering and the direction
comandos=[]
delta=0.001
for point in range(len(path)):
	ex=path[point][0]-bmw.pos_x
	ey=path[point][1]-bmw.pos_y
	eth=atan2(ey,ex)-bmw.angle
	degrees=eth*180/pi
	#Control output:
	#Aqui van ls comandos del carrito
	if degrees>0:
		degrees=int(degrees+delta)
	elif degrees<0:
		degrees=int(degrees-delta)

	if degrees==180.0 or degrees==-180.0:
		#print bmw.pos_x,bmw.pos_y
		bmw.vel=0
		bmw.vel_an=0
		degrees=bmw.vel_an*180/pi
		bmw.update()
		bmw.vel_an=0
		bmw.vel=-1
		bmw.update()
	else:
		bmw.vel=0
		bmw.vel_an=eth
		#degrees=bmw.vel_an*180/pi
		bmw.update()
		bmw.vel_an=0
		bmw.vel=1
		bmw.update()
	if point==len(path)-1:
		bmw.vel=0

	comandos.append([angle_correction(degrees),bmw.vel])
	bmw.plot_robot()

plt.xlim([-1,x])
plt.ylim([-1,y])

plt.show()
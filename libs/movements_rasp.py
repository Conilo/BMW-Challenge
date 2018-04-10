from math import *
import robot_model_rasp as rb
import mappingBMW_rasp as mbmw

def angle_correction(angle):
	x={0:0,90:90,360:0,-360:0,270:-90,-270:90,-90:-90,180:180,-180:180}
	return x[angle]

#Simulacion cajas
roja=mbmw.Caja('red','h',5,1)
azul=mbmw.Caja('blue','v',1,2)
verde=mbmw.Caja('green','h',5,6)
amarilla=mbmw.Caja('yellow','v',1,5)
#Boxes junction
cajas=[roja,verde,azul,amarilla]

#Car simulation
#Initial conditions
bmw=rb.Unicycle()
bmw.pos_x=0
bmw.pos_y=0
bmw.angle=0
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
for i in cajas:
	grid.update_graph(i.get_coordinates(),i.get_orientation()) 

#Path Generation

#Find the shortest in go to goal mode
path=[]
inicio=(0,0)
fin=(x-1,y-1)
#print inicio, fin
uno=[inicio,cajas[0].get_coordinates()]
dos=[cajas[0].get_coordinates(),cajas[1].get_coordinates()]
tres=[cajas[1].get_coordinates(),cajas[2].get_coordinates()]
cuatro=[cajas[2].get_coordinates(),cajas[3].get_coordinates()]
cinco=[cajas[3].get_coordinates(),fin]

#Find the path
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
	last = path_short[-2:]
	path+=path_short


#path=mbmw.short_mapping(graph,s_path)
#Get the steering and the direction
comandos=[]
delta=0.001
def generate_angles():
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

		bmw.vel=0
		bmw.vel_an=eth
		#degrees=bmw.vel_an*180/pi
		bmw.update()
		bmw.vel_an=0
		bmw.vel=1
		bmw.update()
		comandos.append(angle_correction(degrees))
	return comandos

pepe=generate_angles()
print pepe
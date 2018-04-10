
class mappingBMW(object):
	"""docstring x,y mappgBMW"""
	def __init__(self, x,y):
		self.x=x
		self.y=y

	def mapa(self):
		'''
		This function takes as input the size of the map.
		Returns the graph.
		'''
		d_limit=lambda u,v:[(u,v+1),(u+1,v),(u-1,v)]
		u_limit=lambda u,v:[(u+1,v),(u,v-1),(u-1,v)]
		l_limit=lambda u,v:[(u,v+1),(u+1,v),(u,v-1)]
		r_limit=lambda u,v:[(u,v+1),(u,v-1),(u-1,v)]
		points=lambda u,v:[(u,v+1),(u+1,v),(u,v-1),(u-1,v),]
		self.graph={}
		map_x=[i for i in range(self.x)]
		map_y=[j for j in range(self.y)]

		for i in map_x:
			for j in map_y:
				if i==0:
					self.graph[(i,j)]=l_limit(i,j)
					#print [i,j],l_limit(i,j),set(l_limit(i,j))
				elif j==0:
					self.graph[(i,j)]=d_limit(i,j)
				elif j==self.y-1:
					self.graph[(i,j)]=u_limit(i,j)
				elif i==self.x-1:
					self.graph[(i,j)]=r_limit(i,j)
				else:
					self.graph[(i,j)]=points(i,j)
		#4 Corners correction
		self.graph[(0,0)]=[(0, 1), (1, 0)]
		self.graph[(self.x-1,0)]=[(self.x-1, 1),(self.x-2, 0)]
		self.graph[(0,self.y-1)]=[(1, self.y-1),(0, self.y-2)]
		self.graph[(self.x-1,self.y-1)]=[(self.x-1, self.y-2),(self.x-2, self.y-1)]
		return self.graph
		
	def deleteEdge(self,coordinate1,coordinate2):
		self.graph[coordinate1].remove(coordinate2)
		self.graph[coordinate2].remove(coordinate1)

	def sPath(self):
		s=[]
		line=[]
		for i in range(self.x):
			for j in range(self.y):
				line.append((j,i))
			if i & 1:
				line=line[::-1]
			s+=line
			line=[]
		return s

	def update_graph(self,caja,orientation):
		if orientation=='h':
			if caja[1]==0:
				self.deleteEdge(caja,(caja[0],caja[1]+1))
			elif caja[1]==self.y-1:
				self.deleteEdge(caja,(caja[0],caja[1]-1))
			else:
				self.deleteEdge(caja,(caja[0],caja[1]+1))
				self.deleteEdge(caja,(caja[0],caja[1]-1))
		else:
			if caja[0]==0:
				self.deleteEdge(caja,(caja[0]+1,caja[1]))
			elif caja[0]==self.x-1:
				self.deleteEdge(caja,(caja[0]-1,caja[1]))
			else:
				self.deleteEdge(caja,(caja[0]+1,caja[1]))
				self.deleteEdge(caja,(caja[0]-1,caja[1]))


class Caja(object):
    """docstring for ClassName"""
    def __init__(self, color,orientation,x,y):
        self.x=x
        self.y=y
        self.color = color
        self.orientation=orientation
        if self.orientation=='h':
            self.w=0.7
            self.h=0.5
        else:
            self.w=0.5
            self.h=0.7


    def get_coordinates(self):
    	return (self.x,self.y)

    def get_color(self):
    	return (self.color)
    
    def get_orientation(self):
    	return (self.orientation)

    def get_caja(self,u,v):
    	if u==self.x and v==self.y:
    		return [self.x,self.y,self.color,self.orientation]
    	else:
    		return None

def bfs_paths(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        diff=[item for item in graph[vertex] if item not in path] 
        for next in diff:
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

def shortest_path(graph, start, goal):
    try:
        return next(bfs_paths(graph, start, goal))
    except StopIteration:
        return None

def short_mapping(graph,s_path):
	path=[]
	for i in range(len(s_path)-1):
		path_short=shortest_path(graph,s_path[i],s_path[i+1])[1:]
		path+=path_short
	return path
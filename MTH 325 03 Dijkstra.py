#!/usr/bin/env python

#Takes in a weighted graph as input, returns sum of all edge-weights plus 1.
def infty(graph):
    #Define variables.
    total = 1
    prev_edges = []
    is_prev_edge = 0
    
    #For every key in graph, which we'll call vertex:
    for vertex in graph:
        #For every edge in every vertex (in other wrods, every value in a given key):
        for edge in graph[vertex]:
            #Use a 0-1 variable to check if the given value has already been checked.
            is_prev_edge = 0
            for pEdge in prev_edges:
                #Check the normal and reverse for cases such as A,B or B,A.
                if ((vertex + ',' + edge[0]) == pEdge) or ((edge[0] + ',' + vertex) == pEdge):
                    is_prev_edge = 1
                    break
            #If the edge wasn't listed, add to total.
            if is_prev_edge == 0:
                prev_edges.append(vertex + ',' + edge[0])
                total+=edge[1]
    
    return total

##Takes in a weighted graph as its input and returns a vertex coloring in which 'A' is the coloring with 0 
#and all other vertices are colored with infty.
def initial(graph):
    #A is always 0, so define it as such.
    coloring = {}
    coloring['A'] = 0
    infty_num = infty(graph) #Used a var here to limit function calls.
    
    #If the vertex isn't A, set it equal to the number infty returned.
    for vertex in graph:
        if not vertex == 'A':
            coloring[vertex] = infty_num
            
    return coloring

#Takes a vertex-coloring and a list of vertices, and returns a vertex in the list, whose color is smallest.
def find_min(color, queue):
    #Set the values equal to the first element instead of something large.
    min_color = color[queue[0]]
    min_vertex = queue[0]
    
    #Check each item in the queue, get the value of that key from color, check if it's less than color.
    for item in queue:
        if color[item] < min_color:
            min_color = color[item]
            min_vertex = item
            
    return min_vertex

#Dijksta's algorithm. Gets an initial coloring using the initial function, then uses A as the initial source vertex.
#Proceeds to use while loop to check every next-lowest vertex as the source.
def dijkstra(graph):
    vertex_coloring = initial(graph)
    vertices_to_check = []

    #Make a list of all vertices so that every vertex is used as a source in the algorithm.
    for key in graph.keys():
        vertices_to_check.append(key)
    
    #Use A as the initial source to start.
    for edge in graph['A']: #check every edge A connects to.
	#Compare current value of the vertex with the source vertex + edge weight. Use minimum.
        if (vertex_coloring['A'] + edge[1]) < vertex_coloring[edge[0]]:
            vertex_coloring[edge[0]] = (vertex_coloring['A'] + edge[1])
    
    #Remove A from the list of vertices to check.
    vertices_to_check.remove('A')
    
    #Keep doing this until there are no more vertices to use as the source.
    while not (len(vertices_to_check) == 0):
	next_lowest = find_min(vertex_coloring, vertices_to_check)

	#Go over each edge from the next lowest, with next_lowest being the source. Do the same thing as we did with A above.
	for edge in graph[next_lowest]:
            if (vertex_coloring[next_lowest] + edge[1]) < vertex_coloring[edge[0]]:
                vertex_coloring[edge[0]] = (vertex_coloring[next_lowest] + edge[1]) 
        
        #Remove the current source vertex from the vertices to check list.
        vertices_to_check.remove(next_lowest)

    return vertex_coloring

#Tests whether a given graph is connected. Does this by running dijkstra's, and checking if any vertex is unchanged.
#If it is unchanged, it will still be whatever the function infty produces.
def is_connected(graph):
	d_graph = dijkstra(graph)
	gmax = infty(graph)

	for vertex in d_graph:
		if d_graph[vertex] == gmax:
			return False
	return True

graph = {'A' : [['B', 10], ['D', 5]], 'B' : [['A', 10], ['C', 5]], 'C' : [['B', 5], ['D', 15]], 'D' : [['C', 15], ['A', 5]]}
dgraph = {'A' : [['B', 10], ['D', 5]], 'B' : [['A', 10], ['C', 5]], 'C' : [['B', 5], ['D', 15]], 'D' : [['C', 15], ['A', 5]], 'E' : [['F', 5]], 'F' : [['E', 5]]}

infty(graph)
initial(graph)
color = {'A' : 30,'B' : 10, 'C' : 10, 'D' : 15}
queue = ['B', 'C', 'D']
find_min(color, queue)
dijkstra(dgraph)
print(is_connected(graph))

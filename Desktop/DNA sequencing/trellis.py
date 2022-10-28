
def trellis_dp(recieved,transmitted,my_graph):

    return








def bfs(starting_node,my_graph,edges):
    '''my_graph : {'a':['b','c']} etc
       edges = {('a','b) = Pi} etc'''


    queue = [(starting_node,0)]

    output = {node:0 for node in my_graph}

    while queue:
        node,value = queue.pop()

        output[node] += value


        neighbours = my_graph[node]

        for neighbour in neighbours:
            return


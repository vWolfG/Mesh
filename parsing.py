import igraph as ig
import numpy as np
import json

def draw_graph(graph_dict):
        vertices = []
        edges = []
        for i in range(0,len(graph_dict)):
                vertices.append(str(i))
        
        for key in graph_dict:
                for val in graph_dict[key]:
                        tuple_ = (int(key),val)
                        revers_tuple = tuple_[::-1]
                        if revers_tuple not in edges:
                                edges.append(tuple_)
                
        
        g = ig.Graph(vertex_attrs={"label": vertices}, edges=edges, directed=False)
        
        visual_style = {}

        # Scale vertices based on degree
        indegree = g.indegree()
        visual_style["vertex_size"] = [x/max(indegree)*50+110 for x in indegree]

        #layout = g.layout("kk")
        ig.plot(g)
        

# two = {}
# my_list = [None]*10

# my_list[3] = 'lolo'

# print(my_list.index('lolo'))
# print(my_list)
# two['1'] = list()
# print(two, 'efe' + json.dumps(two), json.loads(json.dumps(two)))

# ex = {'0': [1,2], '1':[0], '2':[0,1], '3':[0]}
# #draw_graph(ex)
# str_dict = json.dumps(ex) 

# my_dict = json.loads(str_dict)

# print(str_dict, my_dict)
# print(my_dict['1'])

dicti = {'0': [1,2], '1':[0], '2':[0,1], '3':[0]}
for i, key in dicti.items():
        print(key)


# str_ = "134" + json.dumps(dicti)


# word = list(''.join(str_.split()))
# print(word)
# word2= word[3:]
# print(word2)
# str_1 = ''.join(word2)
# print(json.loads(''.join(word[3:])))
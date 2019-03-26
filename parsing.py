import igraph as ig
import numpy as np

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
        


ex = {'0': [1,2], '1':[0], '2':[0,1], '3':[0]}
draw_graph(ex)
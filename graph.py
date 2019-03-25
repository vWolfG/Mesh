import igraph as ig
def draw_graph(v):
    g = ig.Graph()
    g.add_vertices(v)
#g.add_edges([(1,2), (0,1), (2,0)])
    layout = g.layout()
    ig.plot(g, layout = layout)
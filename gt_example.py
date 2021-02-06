import graph_tool.all as gt
from graph_tool.util import find_vertex
import numpy as np
from numpy.random import random

import matplotlib

# def h(v, target, state):
#     return sum(abs(state[v].a - target)) / 2

class HammingVisitor(gt.AStarVisitor):

    def __init__(self, g, target, state, weight, dist, cost):
        self.g = g
        self.state = state
        self.target = target
        self.weight = weight
        self.dist = dist
        self.cost = cost
        self.visited = {}

    def examine_vertex(self, u):
        for i in range(len(self.state[u])):
            nstate = list(self.state[u])
            nstate[i] ^= 1
            if tuple(nstate) in self.visited:
                v = self.visited[tuple(nstate)]
            else:
                v = self.g.add_vertex()
                self.visited[tuple(nstate)] = v
                self.state[v] = nstate
                self.dist[v] = self.cost[v] = float('inf')
            for e in u.out_edges():
                if e.target() == v:
                    break
                else:
                    e = self.g.add_edge(u, v)
                    self.weight[e] = random()
        self.visited[tuple(self.state[u])] = u

    def edge_relaxed(self, e):
        if self.state[e.target()] == self.target:
            self.visited[tuple(self.target)] = e.target()
            raise gt.StopSearch()

def h(v, target, pos):
    return np.sqrt(sum((pos[v].a - pos[target].a) ** 2))

class VisitorExample(gt.AStarVisitor):

    def __init__(self, touched_v, touched_e, target):
        self.touched_v = touched_v
        self.touched_e = touched_e
        self.target = target

    def discover_vertex(self, u):
        self.touched_v[u] = True

    def examine_edge(self, e):
        self.touched_e[e] = True


    def edge_relaxed(self, e):
        if e.target() == self.target:
            raise gt.StopSearch()


class VeniceResident(gt.AStarVisitor):

    def __init__(self, g, touched_v, touched_e, target, weight):
        self.g = g
        self.weight = weight
        self.touched_v = touched_v
        self.touched_e = touched_e
        self.target = target

    def discover_vertex(self, u):
        self.touched_v[u] = True

    def examine_edge(self, e):
        # cambiamo il peso prendendo da venice_weight
        self.touched_e[e] = True
        #print("ponte ", g.ep['ponte'][e])
        if g.ep['ponte'][e]:
            #print("lunghezza ", g.ep['length'][e])
            self.weight = g.ep['length'][e] #* 20000

    def edge_relaxed(self, e):
        if e.target() == self.target:
            raise gt.StopSearch()

if __name__ == "__main__":
    # g = gt.Graph(directed=False)
    #
    # points = random((500, 2)) * 4
    #
    # points[0] = [-0.01, 0.01]
    # points[1] = [4.01, 4.01]
    #
    # g, pos = gt.triangulation(points, type="delaunay")
    # weight = g.new_edge_property("double") # Edge weights corresponding to
    #                                        # Euclidean distances
    #
    # for e in g.edges():
    #    weight[e] = np.sqrt(sum((pos[e.source()].a - pos[e.target()].a) ** 2))
    graph_path = '/Volumes/Maxtor/Venezia/data/OpenDataVenezia/dequa_ve_shp/terra/v13/dequa_ve_terra_v13_1711.gt'

    g = gt.load_graph(graph_path)

    pos = g.vp['latlon']

    def h(v, target, pos):
        return np.sqrt(sum((pos[v].a - pos[target].a) ** 2))

    touch_v = g.new_vertex_property("bool")
    touch_e = g.new_edge_property("bool")
    venice_weight = g.new_edge_property("double")
    # paretnza 45.43988044474121   12.339807563546461
    # arrivo 45.43170127993013 12.325036058157616
    #coord_source = [12.339807563546461, 45.43988044474121]
    #coord_target = [12.325036058157616, 45.431701279930130]
    latlon = g.vertex_properties['latlon']
    # source = find_vertex(g, latlon, coord_source)
    # target = find_vertex(g, latlon, coord_target)
    # print(f'Source {source}')
    # print(f'Target {target}')
    source = g.vertex(25)
    target = g.vertex(100)

    dist, pred = gt.astar_search(g, source, venice_weight,
                             VeniceResident(g, touch_v, touch_e, target, venice_weight),
                             heuristic=lambda v: h(v, target, pos))
                             # implicit=True
    ecolor = g.new_edge_property("string")
    ewidth = g.new_edge_property("double")
    ewidth.a = 1

    for e in g.edges():
       ecolor[e] = "#3465a4" if touch_e[e] else "#d3d7cf"

    v = target

    while v != source:
        p = g.vertex(pred[v])
        for e in v.out_edges():
            if e.target() == p:
                ecolor[e] = "#a40000"
                ewidth[e] = 30
        v = p

    gt.graph_draw(g, pos=pos, output_size=(20000, 20000), ink_scale=0.1, vertex_fill_color=touch_v,
                  vcmap=matplotlib.cm.binary, edge_color=ecolor, nodefirst=True,
                  edge_pen_width=ewidth, output="astar-dequa-0k.png")

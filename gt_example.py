import graph_tool.all as gt
from graph_tool.util import find_vertex
import numpy as np
from numpy.random import random

import time

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

def distance_from_a_list_of_geo_coordinates(thePoint, coordinates_list):
    """
    A python implementation from the answer here https://stackoverflow.com/questions/639695/how-to-convert-latitude-or-longitude-to-meters.
    Calculate the distance in meters between 1 geographical point (longitude, latitude) and a list of geographical points (list of tuples) or between 2 geographical points passing through distance_from_point_to_point
    """
    # maybe we need to invert
    lat_index = 1
    lon_index = 0
    # parameters
    earth_radius = 6378.137; # Radius of earth in KM
    deg2rad = np.pi / 180
    # single point
    lat1 = thePoint[lat_index] * deg2rad
    lon1 = thePoint[lon_index] * deg2rad
    # test the whole list again the single point
    lat2 = coordinates_list[:,lat_index] * deg2rad
    lon2 = coordinates_list[:,lon_index] * deg2rad
    dLat = lat2 - lat1
    dLon = lon2 - lon1
    a = np.sin(dLat/2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dLon/2) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    d = earth_radius * c
    distances_in_meters = d * 1000

    return distances_in_meters

def find_closest_vertices(coord_list,vertices_latlon_list, MIN_DIST_FOR_THE_CLOSEST_NODE=100):
    """
    Returns list of nodes in vertices_latlon_list closest to coordinate_list (euclidean distance).
    """
    nodes_list=[]
    for coordinate in coord_list:
        # coordinate = np.asarray(d.get("coordinate"))
        #time1 = time.time()
        #tmp = np.subtract(np.ones(G_array.shape) * coordinate, G_array)
        #dists = np.sum(np.sqrt(tmp * tmp), axis=1)
        time2 = time.time()
        dists = distance_from_a_list_of_geo_coordinates(coordinate, vertices_latlon_list)
        time3 = time.time()
        # app.logger.debug("it took {} to calculate distances".format(time3-time2))
        print(f"it took {time3-time2} to calculate distances")
        #dists=d.get("shape").distance(G_array)
        closest_id = np.argmin(dists)
        closest_dist = dists[closest_id]
        # app.logger.debug("il tuo nodo è distante {}".format(closest_dist))
        print(f"il tuo nodo è distante {closest_dist}")
        # se la distanza e troppo grande, salutiamo i campagnoli
        if closest_dist>MIN_DIST_FOR_THE_CLOSEST_NODE:
            # app.logger.error("Sei troppo distante da Venezia, cosa ci fai là?? (il punto del grafo piu vicino dista {} metri)".format(closest_dist))
            print("Sei troppo distante da Venezia, cosa ci fai là?? (il punto del grafo piu vicino dista {closest_dist} metri)")
            # raise custom_errors.UserError("Non abbiamo trovato nulla qua - magari cercavi di andare fuori venezia o forse vorresti andare in barca?")
            return []
        nodes_list.append(closest_id)

    return nodes_list#, dists

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
    graph_path = '/Users/ale/Documents/Venezia/MappaDisabili/v13/dequa_ve_terra_v13_1711.gt'

    g = gt.load_graph(graph_path)

    pos = g.vp['latlon']

    all_pos = np.array([pos[v].a for v in g.iter_vertices()])

    map_coords = [np.array([12.331366730532233, 45.43670740765949])]

    id_closest_vertex = find_closest_vertices(map_coords, all_pos)

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

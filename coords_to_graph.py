#import networkx
# una libreria per leggere gli shapefile --> info qui: http://geopandas.org/index.html
import geopandas as gpd
# per i poligoni
import shapely
# per i grafici
import matplotlib.pyplot as plt
# per il debug
import pdb
# per le cartelle
import os
import numpy as np
import math

def dist2d(p1, p2):

    #pdb.set_trace()
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

if __name__ == '__main__':

    #pdb.set_trace()
    folder = os.getcwd()
    streets_graph = gpd.read_file(folder + "/data" + "/EL_STR.shp")

    points = np.zeros((150000,2))
    cp = 0
    pol_n = 0
    # these will be only unique points, and in the graph the node X will have the coordinates
    # to be found at points_at_nodes[x,:]. The graph will work without coordinates, it does not
    # need them!
    points_as_nodes = np.zeros((150000,2))
    nn = 0
    # here we save the edges as node1, node2, weight (the distance)
    weigh_edges = np.zeros((500000, 3))
    ne = 0

    print("we have {} polygons..".format(len(streets_graph['geometry'])))
    for polygon in streets_graph['geometry']:

        #if pol_n > 25300:
        #    pdb.set_trace()
        if pol_n % 10 == 0 and pol_n > 0:
            print("converting the {}-th".format(pol_n))
        #print(polygon)
        #print(polygon.coords.xy)
        if type(polygon) == shapely.geometry.multilinestring.MultiLineString:
            
            for linestring in polygon:

                start = linestring.coords.xy[0][0], linestring.coords.xy[0][1]
                end = linestring.coords.xy[-1][0], linestring.coords.xy[-1][1]
                alreadyThere = False
                finished = False
                candidates = [start, end]
                indices_nodes = np.zeros((2)).astype(int)
                for k in range(len(candidates)):
                    candidate_node = candidates[k]
                    while not (alreadyThere or finished):
                        for l in range(nn):
                            if (candidate_node[0] - points_as_nodes[l,0])**2 + (candidate_node[1] - points_as_nodes[l,1])**2 < 0.0001:
                                alreadyThere = True
                                indices_nodes[k] = l
                        finished = True
                    if not alreadyThere:
                        points_as_nodes[nn,:] = candidate_node
                        indices_nodes[k] = nn
                        nn += 1

                    if k > 0:
                        #pdb.set_trace()
                        weight = dist2d(points_as_nodes[indices_nodes[k-1]], points_as_nodes[indices_nodes[k]])
                        weigh_edges[ne,:] = [indices_nodes[k-1], indices_nodes[k], weight]
            
                # xs = np.asarray(linestring.coords.xy[0][:]).transpose()
                # ys = np.asarray(linestring.coords.xy[1][:]).transpose()
                # points[cp:cp+len(xs), 0] = xs
                # points[cp:cp+len(ys), 1] = ys
                # cp += len(xs)
                # pol_n += 1
                # indices_nodes = np.zeros((len(xs))).astype(int)
                # for i in range(len(xs)):
                #     candidate_node = [xs[i], ys[i]]
                #     alreadyThere = False
                #     finished = False
                #     while not (alreadyThere or finished):
                #         for l in range(nn):
                #             if (candidate_node[0] - points_as_nodes[l,0])**2 + (candidate_node[1] - points_as_nodes[l,1])**2 < 0.0001:
                #                 alreadyThere = True
                #                 indices_nodes[i] = l
                #         finished = True
                #     if not alreadyThere:
                #         points_as_nodes[nn,:] = candidate_node
                #         indices_nodes[i] = nn
                #         nn += 1

                #     if i > 0:
                #         #pdb.set_trace()
                #         # lenght di shapely
                #         weight = dist2d(points_as_nodes[indices_nodes[i-1]], points_as_nodes[indices_nodes[i]])
                #         weigh_edges[ne,:] = [indices_nodes[i-1], indices_nodes[i], weight]

        elif type(polygon) == shapely.geometry.linestring.LineString:

            linestring = polygon

            start = linestring.coords.xy[0][0], linestring.coords.xy[0][1]
            end = linestring.coords.xy[-1][0], linestring.coords.xy[-1][1]
            alreadyThere = False
            finished = False
            candidates = [start, end]
            indices_nodes = np.zeros((2)).astype(int)
            for k in range(len(candidates)):
                candidate_node = candidates[k]
                while not (alreadyThere or finished):
                    for l in range(nn):
                        if (candidate_node[0] - points_as_nodes[l,0])**2 + (candidate_node[1] - points_as_nodes[l,1])**2 < 0.0001:
                            alreadyThere = True
                            indices_nodes[k] = l
                    finished = True
                if not alreadyThere:
                    points_as_nodes[nn,:] = candidate_node
                    indices_nodes[k] = nn
                    nn += 1

                if k > 0:
                    #pdb.set_trace()
                    weight = dist2d(points_as_nodes[indices_nodes[k-1]], points_as_nodes[indices_nodes[k]])
                    weigh_edges[ne,:] = [indices_nodes[k-1], indices_nodes[k], weight]
            
        if cp > .9 * points.shape[0]:
            tmp = points[:cp,:]
            points = np.zeros((np.round(points.shape[0]*1.5).astype(int), 2))
            points[:cp, :] = tmp        
        
        #     linestring = polygon
        #     xs = np.asarray(linestring.coords.xy[0][:]).transpose()
        #     ys = np.asarray(linestring.coords.xy[1][:]).transpose()
        #     points[cp:cp+len(xs), 0] = xs
        #     points[cp:cp+len(ys), 1] = ys
        #     cp += len(xs)
        #     pol_n += 1
        #     indices_nodes = np.zeros((len(xs))).astype(int)
        #     for i in range(len(xs)):
        #         candidate_node = [xs[i], ys[i]]
        #         alreadyThere = False
        #         finished = False
        #         while not (alreadyThere or finished):
        #             for l in range(nn):
        #                 if (candidate_node[0] - points_as_nodes[l,0])**2 + (candidate_node[1] - points_as_nodes[l,1])**2 < 0.0001:
        #                     alreadyThere = True
        #                     indices_nodes[i] = l
        #             finished = True
        #         if not alreadyThere:
        #             points_as_nodes[nn,:] = candidate_node
        #             indices_nodes[i] = nn
        #             nn += 1

        #         if i > 0:
        #             #pdb.set_trace()
        #             weight = dist2d(points_as_nodes[indices_nodes[i-1]], points_as_nodes[indices_nodes[i]])
        #             weigh_edges[ne,:] = [indices_nodes[i-1], indices_nodes[i], weight]
            
        # if cp > .9 * points.shape[0]:
        #     tmp = points[:cp,:]
        #     points = np.zeros((np.round(points.shape[0]*1.5).astype(int), 2))
        #     points[:cp, :] = tmp        
        #print(streets_graph[column].head())
    G = nx.graph()

    pdb.set_trace()
    plt.scatter(points[:,0], points[:,1])
    pdb.set_trace()


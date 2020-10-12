##### salva in pickle il gpd finale (strade). SHP deve già essere om WSG4
import geopandas as gpd
import networkx as nt
import pickle
import os
import sys
import datetime
import pdb
import shapely.wkt as wkt
import numpy as np

cl_folder = "/Users/Palma/Documents/Projects/Venessia4Working/Venessia4Working/data"
cl_path = os.path.join(cl_folder, "curve_di_livello_dequa_crs.shp")
curve_di_livello = gpd.read_file(cl_path)
curve_di_livello['geometry'][0]
geom_curves = curve_di_livello['geometry']

#archi
archi_path = os.path.join(cl_folder, "dequa_ve_terra_v9_0910.shp")
archi = gpd.read_file(archi_path)

#envelope per shapely
envelope_path = os.path.join(cl_folder, "TP_STR.shp")
envelopes = gpd.read_file(envelope_path)

from shapely.ops import voronoi_diagram
---------------------------------------------------------------------------
ImportError                               Traceback (most recent call last)
<ipython-input-17-d679c671ffc0> in <module>
----> 1 from shapely.ops import voronoi_diagram

ImportError: cannot import name 'voronoi_diagram' from 'shapely.ops' (/opt/anaconda3/lib/python3.7/site-packages/shapely/ops.py)

for geom_polygon, polygon_id in envelopes[['geometry','CVE_SCOD_V']].values:

    edges = archi[archi['street_id']==polygon_id]

    print(len(edges))
    print(edges)
    geom_edges = edges['geometry']
    voronoi_diagram(geom_edges, geom_polygon)
    break
    voronoi_diagram

folder = "/Users/Palma/Documents/Githubs/v4w_website/app/static/files"
path_graph = os.path.join(folder, 'dequa_ve_terra_v8_dequa_ve_terra_0509_pickle_4326VE')
with open(path_graph, 'rb') as file:
    G_un = pickle.load(file)
G_un

# ciclo for su ogni arco
# PSEUDOCODICE:
# for each edge:
#    prendiamo la linea dell'arco
#    costruiamo una griglia di linee perpendicolari all'arco (in modo da avere la geometria)
#    per ogni linea perpendicolare:
#       fetchiamo massimo e minimo
#       intersezione tra le curve di livello e la linea perpendicolare
#    una volta finite le linee:
#       scegliamo massimo e minimo per arco e lo salviamo come attributo dell'arco
#       calcoliamo una media/mediana e la salviamo?
#    (opzionale):
#    guardiamo il nome e salviamo il nome della strada come attributo dell'arco

# parametri:
distance_sampling = 10e-7 # metro
from pprint import pprint
# ciclo for degli archi
for edge_coords in G_un.edges():
    # linea
    edge = G_un[edge_coords[0]][edge_coords[1]]
    geometry_edge = wkt.loads(edge['Wkt']).coords
    street_id = edge['street_id']
    if len(geometry_edge) < 2:
        raise Exception('The Edge is a point (???)')
    for idx_segment in range(len(geometry_edge)-1):
        segment = [geometry_edge[idx_segment], geometry_edge[idx_segment+1]]
        print(segment)
        # sampling della linea
        start_point = segment[0]
        end_point = segment[-1]
        length_segment = edge['length'] # in metri
        distance_points = np.sqrt(np.sum(np.power(np.subtract(end_point, start_point), 2)))
        print("dist: ", distance_points)
        num_steps = np.floor(distance_points/distance_sampling).astype(int)
        print("steps: ", num_steps)
        direction_vector = (np.subtract(end_point, start_point)) / num_steps
        rot_anti = np.array([[0, -1], [1, 0]])
        direction_vector_perp = np.dot(rot_anti, direction_vector) * 10e-5
        print("direction ", direction_vector)
        for n in range(num_steps):
            cur_sampling_point = start_point + n * direction_vector
            linestring_direction_perp = shapely.geometry.LineString([cur_sampling_point-direction_vector_perp, cur_sampling_point+direction_vector_perp])
            for j in range(len(geom_curves)):
                print(j)
                curve = geom_curves[j]
                intersection_ = curve.intersection(linestring_direction_perp)
                if (intersection_):
                    print("intersection between {} and {}".format(curve, linestring_direction_perp))
                    pprint(intersection_)

                print("finished")
            break
        break
    break
break
            #perp_line =

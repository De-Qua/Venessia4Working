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
curve_di_livello


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
distance_sampling = 0.1 # metro

# ciclo for degli archi
for edge_coords in G_un.edges():
    # linea
    edge = G_un[edge_coords[0]][edge_coords[1]]

    geometry_edge = wkt.loads(edge['Wkt']).coords
    for segment in geometry_edge:
        print(segment)
        # sampling della linea
        start_point = segment[0]
        end_point = segment[-1]
        distance_points = np.sqrt(np.sum(np.power(end_point-start_point, 2)))
        num_steps = np.floor(distance_points/distance_sampling).astype(int)
        direction_vector = (end_point - start_point) / num_steps
        print(direction_vector)
        for n in range(num_steps):
            cur_sampling_point = start_point + n * direction_vector
            break

        break
    break
break
            #perp_line =

import networkx
# una libreria per leggere gli shapefile --> info qui: http://geopandas.org/index.html
import geopandas as gpd
# per i grafici
import matplotlib.pyplot as plt
# per il debug
import pdb
# per le cartelle
import os

pdb.set_trace()
folder = os.getcwd()
streets_graph = networkx.readwrite.nx_shp.read_shp(folder + "/data" + "/EL_STR.shp")
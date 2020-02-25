from dijkstar import Graph, find_path
import pandas as pd
# una libreria per leggere gli shapefile --> info qui: http://geopandas.org/index.html
import geopandas as gpd
# per i grafici
import matplotlib.pyplot as plt
# per il debug
import pdb
# per le cartelle
import os
import sys
sys.path.append('/home/lucatastrophe/Desktop/venessia/Venessia4Working-master')
# metodo per avere gli indici delle vie o della via trovata
from mydifflib import get_close_matches_indexes
from networkx import readwrite


folder = os.getcwd()
streets_graph = gpd.read_file(folder + "/Venessia4Working/data" + "/EL_STR.shp")
streets_names = gpd.read_file(folder + "/Venessia4Working/data" + "/TP_STR.shp")
#civico = gpd.read_file(folder + "/data" + "/CIVICO.shp")

pesi = streets_graph['geometry'].length
bounds = streets_graph['geometry'].boundary
Xbound1 = []
Ybound1 = []
Xbound2 = []
Ybound2 = []
i=0
for bound in bounds:
    i=i+1;
    try:
        Xbound1.append(bound[0].x)
        Ybound1.append(bound[0].y)
        Xbound2.append(bound[1].x)
        Ybound2.append(bound[1].y)
    except:
        print('coordinate not found for element',i)
        Xbound1.append(0)
        Ybound1.append(0)
        Xbound2.append(0)
        Ybound2.append(0)
        
nodes = pd.DataFrame({'X1':Xbound1,
                      'Y1':Ybound1,
                      'X2':Xbound2,
                      'Y2':Ybound2,
                      'pesi':pesi})

doubles = nodes['X1'].duplicated()

graph = Graph()
graph.add_edge(1, 2, 110)
graph.add_edge(2, 3, 125)
graph.add_edge(3, 4, 108)
find_path(graph, 1, 4)

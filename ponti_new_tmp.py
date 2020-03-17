# %% codecell
# Import all packages

# una libreria per leggere gli shapefile --> info qui: http://geopandas.org/index.html
import geopandas as gpd
# per i grafici
import matplotlib.pyplot as plt
# per il debug
import pdb
# per le cartelle
import os
#test per il push
import networkx as nt
from networkx.exception import NetworkXNoPath
import numpy as np
#libreria per leggere gli attributi degli edge
import json
#libreria per convertire da Json a shapely
from shapely.geometry import mapping, shape
#utility per coordinates
from library_coords import civico2coord
# %% codecell
plt.ion()

folder = os.getcwd()
ponti = gpd.read_file(folder+"/pontiDivisi_completo/pontiDivisi_solo_venezia.shp")

G = nt.read_shp(folder + "/pontiDivisi_completo/pontiDivisi_solo_venezia.shp")
#il file zona_22 è stato formattato con new_gpd_to_graph (aggiunti pesi e tolte colonne inutili)

# se vogliamo accedere ai nodi con degli indici
#G_2 = nt.convert_node_labels_to_integers(G)

# per renderlo bidirezionale
#G_un_2 = G_2.to_undirected()
G_un = G.to_undirected()
G_list = list(G_un.nodes)

# disegna il grafo le coordinate sono a caso
nt.draw(G_un)

# %% codecell
# Plot the shape file

ponti.plot()
# %% codecell
# crea un dizionario con la corrispondenza nodo-coordinata (se uso grafo senza indici il nodo è identificato proprio dalla coordinata. Viene fuori coordinata:coordinata
pos = dict(zip([v for v in G_un.nodes()], [f for f in G.nodes()]))
nt.draw_networkx(G_un, pos, node_size = 40, node_color = "y", edge_color = "y", font_size = 8)


# %% codecell
# weight_bridge come funzione peso
def weight_bridge(x,y,dic):
#    if dic["altezza"]< 110:
#        w = 100
#    else:
#        w=0
    return dic["length"] + dic["ponte"]*100
    #weight = dic["length"] if dic["ponte"]==0 else None
 #   return weight

# %% codecell
def plot_shortest_path(path_nodes,map_shp):
    # path_nodes lista di nodi attraversati
    # map_shp shapefile generale della mappa su cui si cerca il percorso

    # Converte la lista di nodi in file json
    shapes = []
    for i in range(len(path_nodes)-1):
        shapes.append(shape(json.loads(G_un[path_nodes[i] ][path_nodes[i+1] ]['Json'])))
    x_tot = []
    for sha in shapes:
    #   print(sha.coords.xy)
        x = []
        for i in range(len(sha.coords.xy[0])):
            x.append((sha.coords.xy[0][i],sha.coords.xy[1][i]))
        # to be corrected with x_start
        if not x_tot:
            x_tot+=x
        elif x[0] == x_tot[-1]:
    #        print(x[0], "uguali",x_tot[-1])
            x_tot+=x
        else:
    #        print(x[0],"diversi", x_tot[-1])
            x_tot+=x[::-1]

    x_tot = np.asarray(x_tot)
    plt.figure()
    map_shp.plot()
    plt.plot(x_tot[:,0], x_tot[:,1], c="r")
    return
# %% codecell
civico = gpd.read_file(folder + "/data" + "/CIVICO.shp")
try:
    starting_address = input('Da dove parti?\n')
    coord = civico2coord(G_list, starting_address, civico)
    coord2 = civico2coord(G_list, "santa croce, 343", civico)
    # Dijkstra algorithm, funzione peso lunghezza
    G_un[coord]
    path = nt.algorithms.shortest_paths.weighted.dijkstra_path(G_un,coord,coord2, weight="length")
    # lista dei nodi attraversati
    path_nodes = [n for n in path]
    plot_shortest_path(path_nodes,ponti)
except NetworkXNoPath:
    print("Non esiste un percorso tra i due nodi")
    ponti.plot()
# %% codecell
# Dijkstra algorithm, funzione peso ponti
try:
    path_nobridges = nt.algorithms.shortest_paths.weighted.single_source_dijkstra(G_un, coord,coord2, weight = weight_bridge)
    # lista dei nodi attraversati
    path_nodes_nobridges = [n for n in path_nobridges[1]]
    plot_shortest_path(path_nodes_nobridges,ponti)
    print(path_nobridges[0])
except NetworkXNoPath:
    print("Non esiste un percorso tra i due nodi")
    ponti.plot()

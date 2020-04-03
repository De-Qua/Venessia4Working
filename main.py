# una libreria per leggere gli shapefile --> info qui: http://geopandas.org/index.html
# per le cartelle
import os
#test per il push
import networkx as nt
from networkx.exception import NetworkXNoPath
import numpy as np
#utility per coordinates
import sys
sys.path.append("/home/lucatastrophe/Desktop/venessia/Venessia4Working/lib")
from library_coords import civico2coord
from weights_libs import weight_bridge

folder = os.getcwd()
G = nt.read_shp(folder + "/databases/pontiDivisi_solo_venezia_l.shp")
# per renderlo bidirezionale
G_un = G.to_undirected()
G_list = list(G_un.nodes)
# carica lista degli indirizzi con relativa posizione
civico = np.loadtxt("lista_civici_csv.txt", delimiter = ";" ,dtype='str')
## TODO: AGGIUNGI LA POSSIBILITA DEI TOPONIMI NELLA RICERCA
toponimo =  np.loadtxt("lista_toponimi_csv.txt", delimiter = ";" ,dtype='str')
coords = np.loadtxt("lista_coords.txt")


#civico = np.loadtxt(folder+"/civico_tot.txt")

# definizione di partenza e arrivo (da implementare con search bar e deve ammettere i click sulla mappa)
# per ora usiamo solo i civici, i toponimi sono ancora da fare
starting_address = input('Da dove parti?\n')
coord = civico2coord(G_list, starting_address, civico, coords)
ending_address = input('Dove vai?\n')
coord2 = civico2coord(G_list, ending_address, civico, coords)

# Dijkstra algorithm, funzione peso lunghezza
try:
    path = nt.algorithms.shortest_paths.weighted.dijkstra_path(G_un,coord,coord2, weight="length")
    # lista dei nodi attraversati
    path_nodes = [n for n in path]
except NetworkXNoPath:
    print("Non esiste un percorso tra i due nodi")
# %% codecell
# Dijkstra algorithm, funzione peso ponti
try:
    length_path, path_nobridges = nt.algorithms.shortest_paths.weighted.single_source_dijkstra(G_un, coord,coord2, weight = weight_bridge)
    # lista dei nodi attraversati
    path_nodes_nobridges = [n for n in path_nobridges]
    #print(length_path)
except NetworkXNoPath:
    print("Non esiste un percorso tra i due nodi")

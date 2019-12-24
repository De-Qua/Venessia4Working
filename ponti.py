#questo script mi serve solo per selezionare le colonne che mi interessano del GeoDataFrame e salvarle in un nuovo file che contiene 2 strutture: indirizzo e coordinata; l'altra toponimo centroide . Inoltre deve salvare in numpy un array di nomi (sestieri e toponimi). 

# una libreria per leggere gli shapefile --> info qui: http://geopandas.org/index.html
import geopandas as gpd
# per i grafici
import matplotlib.pyplot as plt
# per il debug
import pdb
# per le cartelle
import os
# metodo per avere gli indici delle vie o della via trovata
from mydifflib import get_close_matches_indexes
import networkx as nt

from string import maketrans


folder = os.getcwd()
ponti = gpd.read_file("/home/lucatastrophe/Desktop/venessia/Venessia4Working/zona_con_ponti/zona_2.shp")

venezia_ind  = ponti["INDIRIZZO"].str.contains( "DORSODURO")
G = nt.read_shp("/home/lucatastrophe/Desktop/venessia/Venessia4Working/zona_con_ponti/zona_22.shp")
#il file zona_22 è stato formattato con new_gpd_to_graph (aggiunti pesi e tolte colonne inutili)


# se vogliamo accedere ai nodi con degli indici
G_2 = nt.convert_node_labels_to_integers(G)

# per renderlo bidirezionale
G_un = G_2.to_undirected()

# disegna il grafo le coordinate sono a caso
nt.draw(G_un)

# crea un dizionario con la corrispondenza nodo-coordinata (se uso grafo senza indici il nodo è identificato proprio dalla coordinata. Viene fuori coordinata:coordinata
pos = dict(zip([v for v in G_un.nodes()], [f for f in G.nodes()])) 
nt.draw_networkx(G_un, pos)

#libreria per leggere gli attributi degli edge
import Json

# importiamo il Linestring che definisce la strada corrispondente all-edge (1-146)
json.loads(G_un[1][146]['Json'])

#libreria per convertire da Json a shapely
from shapely.geometry import mapping, shape
s = shape(json.loads(G_un[1][146]['Json']))

nt.algorithms.shortest_paths.weighted.dijkstra_path(G_un,890, 207) # ripetere questo percorso con la funzione peso dei ponti
#streets_names = gpd.read_file(folder + "/data" + "/TP_STR.shp")
#civico = gpd.read_file("/home/lucatastrophe/Desktop/venessia/Venessia4Working/data/Tema0301_ToponimiNumeriCivici/CIVICO.shp")

# provato, dovrebbe prendere i pesi ma calcola strade sbagliate
path = nt.algorithms.shortest_paths.weighted.dijkstra_path(G_un, 890, 738, weight = "length")

# dovrebbe essere la formattazione corretta per i label degli edges
labels = dict(zip([v for v in G_un.edges],[G_un[w[0]][w[1]]["length"] for w in G_un.edges]))

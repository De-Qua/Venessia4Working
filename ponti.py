
#questo script contiene un po' di prove fatte con la libreria networkx. Permette infatti di leggere gli shapefile, di convertirli in grafi (che possono avere i nodi definiti dalle coordinate o i nodi indicizzati per accedervi), di disegnarli (con una geometria da grafo che perde le informazioni sulla geografia, oppure con la disposizione che si può sovrapporre allo shapefile), di calcolare la strada più corta tra due nodi, anche usando la funzione peso che per il momento può tenere conto dei ponti ma non dell'acqua alta). La strada più corta è una sequenza di nodi: per estrarre tutte le coordinate che permettono di ricostruire le calli a partire dai nodi ci sono i comandi che usano Json e shapely. ATTENZIONE: Le path sono indicate col formalismo linux del mio pc, andrebbe reso invece universale.

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

import numpy as np

plt.ion()

folder = os.getcwd()
ponti = gpd.read_file("zona_con_ponti/zona_22.shp")

G = nt.read_shp("zona_con_ponti/zona_22.shp")
#il file zona_22 è stato formattato con new_gpd_to_graph (aggiunti pesi e tolte colonne inutili)

# se vogliamo accedere ai nodi con degli indici
G_2 = nt.convert_node_labels_to_integers(G)

# per renderlo bidirezionale
G_un = G_2.to_undirected()

# disegna il grafo le coordinate sono a caso
nt.draw(G_un)

# crea un dizionario con la corrispondenza nodo-coordinata (se uso grafo senza indici il nodo è identificato proprio dalla coordinata. Viene fuori coordinata:coordinata
pos = dict(zip([v for v in G_un.nodes()], [f for f in G.nodes()]))


ponti.plot()
nt.draw_networkx(G_un, pos, node_size = 40, node_color = "y", edge_color = "y", font_size = 8)

#libreria per leggere gli attributi degli edge
import json

# importiamo il Linestring che definisce la strada corrispondente all-edge (1-146), ossia da le coordinate punto per punto della strada
json.loads(G_un[890][895]['Json'])

#libreria per convertire da Json a shapely
from shapely.geometry import mapping, shape
s = shape(json.loads(G_un[890][895]['Json']))

nt.algorithms.shortest_paths.weighted.dijkstra_path(G_un,890, 207) # ripetere questo percorso con la funzione peso dei ponti
#streets_names = gpd.read_file(folder + "/data" + "/TP_STR.shp")
#civico = gpd.read_file("/home/lucatastrophe/Desktop/venessia/Venessia4Working/data/Tema0301_ToponimiNumeriCivici/CIVICO.shp")

# provato, dovrebbe prendere i pesi
path = nt.algorithms.shortest_paths.weighted.dijkstra_path(G_un, 890, 738, weight = "length")

# dovrebbe essere la formattazione corretta per i label degli edges
labels = dict(zip([v for v in G_un.edges],[G_un[w[0]][w[1]]["length"] for w in G_un.edges]))

# Usando weight_bridge come funzione peso
def weight_bridge(x,y,dic):
#    if dic["altezza"]< 110:
#        w = 100
#    else:
#        w=0
    return dic["length"] + dic["ponte"]*2000


def plot_short_path(start, end):
    
    path = nt.algorithms.shortest_paths.weighted.single_source_dijkstra(G_un, start, end, weight = weight_bridge)

    # lista dei nodi
    listadinodi = [G_un[n] for n in path[1]]
    # solo i numeri
    soloinumeri = [n for n in path[1]]
    # archi
    nodo1 = [n for n in path[1][:-1]]
    nodo2 = [n for n in path[1][1:]]
    shapes = []
    for i in range(len(soloinumeri)-1):
        shapes.append(shape(json.loads(G_un[soloinumeri[i] ][soloinumeri[i+1] ]['Json'])))
        #shapes = [shape(json.loads(G_un[a][b]['Json'])) for a,b in [nodo1, nodo2]]

    #x_start = json.loads(G_un[path[1][0]][0]['Json'])
    x_tot = []
    for sha in shapes:
        #   print(sha.coords.xy)
        x = []
        for i in range(len(sha.coords.xy[0])):
            x.append((sha.coords.xy[0][i],sha.coords.xy[1][i]))
            # to be corrected with x_start
        if not x_tot:
            x_tot+=x[::-1]
        elif x[0] == x_tot[-1]:
            #        print(x[0], "uguali",x_tot[-1])
            x_tot+=x
        else:
            #        print(x[0],"diversi", x_tot[-1])
            x_tot+=x[::-1]

    x_tot = np.asarray(x_tot)

    ponti.plot()
    plt.plot(x_tot[:,0], x_tot[:,1], c="r")
    return

pos = nt.spring_layout(G_un)

pos = dict(zip([v for v in G_un.nodes()], [f for f in G.nodes()]))
h = G_un.subgraph(path[1])
ponti.plot()
nt.draw_networkx_nodes(h,pos=pos, node_color='b', node_size=1, node_color = "r") #or even nx.draw(h,pos=pos,node_color='b') to get nodes and edges in one command
nt.draw_networkx_edges(h,pos=pos)

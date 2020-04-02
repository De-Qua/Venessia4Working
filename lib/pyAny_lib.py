import numpy as np
import networkx as nt
from networkx.exception import NetworkXNoPath
import sys
sys.path.append('/home/rafiki/v4w')
#utility per coordinates
from libpy.library_coords import civico2coord_first_result
from libpy.weights_libs import weight_bridge


def init(shp_path, civici_tpn_path, coords_path):
    
    G = nt.read_shp(shp_path)
    G_un = G.to_undirected()
    civici_tpn = np.loadtxt(civici_tpn_path, delimiter = ";" ,dtype='str')
    coords = np.loadtxt(coords_path)
    return G_un, civici_tpn, coords




def calculate_path(G_un, coords_start, coords_end):

    # Dijkstra algorithm, funzione peso lunghezza
    try:
        path = nt.algorithms.shortest_paths.weighted.dijkstra_path(G_un,coords_start,coords_end, weight="length")
        # lista dei nodi attraversati
        path_nodes = [n for n in path]
        print("\n#########\n##TEST1##\n#########")
        print("strada con ponti: ", len(path_nodes), " nodi!")
        print(path_nodes)
    except NetworkXNoPath:
        print("Non esiste un percorso tra i due nodi")
    # %% codecell
    # Dijkstra algorithm, funzione peso ponti
    try:
        length_path, path_nobridges = nt.algorithms.shortest_paths.weighted.single_source_dijkstra(G_un, coords_start,coords_end, weight = weight_bridge)
        # lista dei nodi attraversati
        path_nodes_nobridges = [n for n in path_nobridges]
        #print(length_path)
        print("\n#########\n##TEST2##\n#########")
        print("strada con meno ponti: ", len(path_nodes_nobridges), " nodi!")
        print(path_nodes_nobridges)
        print("lunghezza (in metri, contando 100 metri per ponte: ", length_path)
    except NetworkXNoPath:
        print("Non esiste un percorso tra i due nodi")

    return path_nodes, path_nodes_nobridges, length_path

from mydifflib import get_close_matches_indexes
import networkx as nt
import numpy as np

"""
salva una lista txt delle coordinate. Solo per sicurezza, non verrà mai usata
"""
def salva_lista_coordinate(shapefile_path, txt_path):
    G = nt.read_shp(shapefile_path)
    G_list = list(G.nodes)
    with open(txt_path, 'w') as f:
        for item in G_list:
            f.write(str(item) + "\n")
    return
"""
partita contro Google
https://stackoverflow.com/questions/8527952/nearest-neighbor-search-in-python-without-k-d-tree
"""
def controlla_chi_vince(shapefile_path, q):
    import time
    G = nt.read_shp(shapefile_path)
    G_list = list(G.nodes)
    coordinate = np.asarray(G_list)

    time1 = time.time()
    idx = np.argmin([np.inner(q-x,q-x) for x in coordinate])
    time2 = time.time()
    print(time2-time1)

    time3 = time.time()
    idx2 = np.argmin(np.sum(np.subtract(np.ones((coordinate.shape)) * q, coordinate) * np.subtract(np.ones((coordinate.shape)) * q, coordinate), axis=1))
    time4 = time.time()
    print(time4-time3)

    time5 = time.time()
    tmp = np.subtract(np.ones((coordinate.shape)) * q, coordinate)
    idx3 = np.argmin(np.sum(tmp * tmp, axis=1))
    time6 = time.time()
    print(time6-time5)

    if time2-time1 > time4-time3:
        print("Steve ha vinto!")
    else:
        print("Grande vittoria! Venessia4Working 1 - 0 Google")

"""
decide se e civico o no
"""
def isCivico(stringa):

    return True

"""
inutile
"""
def fintoMain():

    if isCivico:
        civico2coord()
    else:
        toponimo2coord()

"""
trova il nome da una lista
"""
def checkNameFromList(lista, nome):

    matches = get_close_matches_indexes(nome.upper(), lista)
    streets_founds = []
    if streets_list[matches[0]] == nome.upper():
        which_one = 0
    else:
        for i in range(len(matches)):
            streets_founds.append(lista[matches[i]])
            print("Trovato: {}:{}".format(i, streets_founds[i]))
        which_one = int(input("Quale intendi? Scrivi il numero\n"))

    indiceCorretto = matches[which_one]
    nomeCorretto = streets_corrected[indiceCorretto]

    return nomeCorretto, indiceCorretto


"""
controlla il nome e ritorna quello corertto!
"""
def checkNomi(nome, gdp_civico, gpd_toponimo):

    if isCivico(nome):
        lista_toponimi = gpd_civico["INDIRIZZO"].tolist()
        nomeCorretto, indiceCorretto = checkNameFromList(nome, lista_toponimi)
    else:
        lista_civici = gpd_toponimo["TP_STR_NOM"].tolist()
        nomeCorretto, indiceCorretto = checkNameFromList(nome, lista_civici)

    return nomeCorretto, indiceCorretto

"""
ritorna una coordinata (x,y), che e anche la stringa di accesso a un nodo
prende in input il nome corretto!
"""
def nome2coord(coord_list, nome, lista_toponimi):
    coordinate = np.asarray(coord_list)
    coord = gpd_civico['geometry'][indiceCorretto]
    coord_centroid = coord.centroid.bounds[0:2]
    tmp = np.subtract(np.ones((coordinate.shape)) * coord_centroid, coordinate)
    idx = np.argmin(np.sum(tmp * tmp, axis=1))
    return (coordinate[0], coordinate[1])

"""
da toponimo, ritorna una coordinata (x,y), che e anche la stringa di accesso a un nodo
"""
def toponimo2coord(coord_list,civico_name,gpd_toponimo):
    coordinate = np.asarray(coord_list)
    streets_list = gpd_toponimo["TP_STR_NOM"].tolist()
    # removing one (or more) annoying none values
    streets_corrected = [street if street else "" for street in streets_list]
    matches = get_close_matches_indexes(civico_name.upper(), streets_corrected)
    streets_founds = []
    if streets_list[matches[0]] == civico_name.upper():
        which_one = 0
    else:
        for i in range(len(matches)):
            streets_founds.append(streets_list[matches[i]])
            print("Trovato: {}:{}".format(i, streets_founds[i]))
        which_one = int(input("Quale intendi? Scrivi il numero\n"))

    coord = gpd_toponimo['geometry'][matches[which_one]]
    coord_centroid = coord.centroid.bounds[0:2]
    tmp = np.subtract(np.ones((coordinate.shape)) * coord_centroid, coordinate)
    idx = np.argmin(np.sum(tmp * tmp, axis=1))
    return (coordinate[0], coordinate[1])

"""
da civico, ritorna una coordinata (x,y), che e anche la stringa di accesso a un nodo
"""
def civico2coord(coord_list,civico_name,gpd_civico):
    coordinate = np.asarray(coord_list)
    streets_list = gpd_civico["INDIRIZZO"].tolist()
    # removing one (or more) annoying none values
    streets_corrected = [street if street else "" for street in streets_list]
    matches = get_close_matches_indexes(civico_name.upper(), streets_corrected)
    streets_founds = []
    if streets_list[matches[0]] == civico_name.upper():
        which_one = 0
    else:
        for i in range(len(matches)):
            streets_founds.append(streets_list[matches[i]])
            print("Trovato: {}:{}".format(i, streets_founds[i]))
        which_one = int(input("Quale intendi? Scrivi il numero\n"))

    coord = gpd_civico['geometry'][matches[which_one]]
    coord_centroid = coord.centroid.bounds[0:2]
    tmp = np.subtract(np.ones((coordinate.shape)) * coord_centroid, coordinate)
    idx = np.argmin(np.sum(tmp * tmp, axis=1))
    return (coordinate[idx][0], coordinate[idx][1])

"""
arrangia il grafo e la lista dei nodi ricevendo come input il nome del file
"""
def arrangiaTuttoDalloShapefile(shapefile_path):

    G_ = nt.read_shp(shapefile_path)
    G = G_.to_undirected()
    G_list = list(G_un.nodes)

    return G_un, G_list

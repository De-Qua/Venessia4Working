from lib.mydifflib import get_close_matches_indexes
import networkx as nt
import numpy as np


"""
da civico, ritorna una coordinata (x,y), che e anche la stringa di accesso a un nodo
"""
def civico2coord(coord_list,civico_name,gpd_civico):
    coordinate = np.asarray(coord_list)
    streets_list = gpd_civico["INDIRIZZO"].tolist()
    # removing one (or more) annoying none values
    streets_corrected = [street if street else "" for street in streets_list]
    option_number = 1
    matches = get_close_matches_indexes(civico_name.upper(), streets_corrected, option_number)
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



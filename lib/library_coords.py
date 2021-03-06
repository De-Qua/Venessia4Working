from lib.mydifflib import get_close_matches_indexes
import networkx as nt
import numpy as np


"""
da civico, ritorna una coordinata (x,y), che e anche la stringa di accesso a un nodo
"""
def civico2coord(coord_list,civico_name,civico_list, civico_coord):
    coordinate = np.asarray(coord_list)
    # removing one (or more) annoying none values
    #streets_corrected = [street if street else "" for street in streets_list]
    option_number = 3 #rimetto 3 per adesso, poi cambiamo
    matches = get_close_matches_indexes(civico_name.upper(), civico_list, option_number)
    streets_founds = []
    if civico_list[matches[0]] == civico_name.upper():
        which_one = 0
    else:
        for i in range(len(matches)):
            streets_founds.append(civico_list[matches[i]])
            print("Trovato: {}:{}".format(i, streets_founds[i]))
        which_one = int(input("Quale intendi? Scrivi il numero\n"))

    coord = civico_coord[matches[which_one]]
    tmp = np.subtract(np.ones((coordinate.shape)) * coord, coordinate)
    idx = np.argmin(np.sum(tmp * tmp, axis=1))
    return (coordinate[idx][0], coordinate[idx][1])

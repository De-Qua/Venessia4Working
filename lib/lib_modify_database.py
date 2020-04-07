# Per creare il grafo per il sito e i txt con i nomi e le coordinate: - su qgis, convertire in epsg4326 tutti gli shp -civico.shp, EL_STR, TP_STR - (apro civico.shp -l'originale- al dialogo iniziale gli dico di usare epgs3004 -perché così vanno interpretate le sue coordinate- una volta caricata la mappa vado su layer-> "save layer as" e lì gli indico il crs epsg4326), spezzare i ponti (chissà come, ale lo sa) - da questo script, togliere mestre, togliere le colonne inutili, salvare in pickle e aggiornare il txt

import geopandas as gpd
# per i grafici
import matplotlib.pyplot as plt
# per il debug
import pdb
import numpy as np
# per le cartelle
import os
# metodo per avere gli indici delle vie o della via trovata
from mydifflib import get_close_matches_indexes

# limiti di venezia in epsg3004
#x1 2309038 x2 2314037 y1 5033256 y2 5036386

def lista_di_indici_senza_mestre_dalle_coordinate(cx, cy):
    venezia_x = (cx > 12.29).astype(int) * (cx < 12.366).astype(int)
    venezia_y = (cy > 45.422).astype(int) * (cy < 45.45).astype(int)
    venezia = (venezia_x * venezia_y ).astype(bool)
    return venezia


folder = os.getcwd()

########### creiamo il txt concatenato di civico e dei toponimi, togliendo mestre e cambiando le coordinate
# le coordinate TP sono epsg3004 e vanno convertite
TP = gpd.read_file(folder + "/../data_bkp" + "/TP_STR.shp")
# le coordinate di civico devono essere già convertite con QGIS, perché per qualche misterioso motivo non si riesce da codice (probabilmente il file è stato creato male all'origine, senza specificare la proiezione)
civico = gpd.read_file(folder + "/../data_bkp" + "/CIVICO_4326.shp")

civico_centroids = civico["geometry"].centroid
cx = [centroid.x if centroid else 0. for centroid in civico_centroids]
cy = [centroid.y if centroid else 0. for centroid in civico_centroids]

TP = TP.to_crs(epsg=4326)
TP_centroids = TP["geometry"].centroid
cx_TP = [centroid.x if centroid else 0. for centroid in TP_centroids]
cy_TP = [centroid.y if centroid else 0. for centroid in TP_centroids]
cx = np.asarray(cx +cx_TP)
cy = np.asarray(cy+ cy_TP)

#estraggo le altre informazioni rilevanti
new_civico_names = civico["INDIRIZZO"]
# "denominazi" sarebbe da aggiungere
new_civico_toponimo = civico["DENOMINAZI"]
TP_names = TP["TP_STR_NOM"]
names_tot = new_civico_names.append(TP_names)
names_tot = new_civico_names.append(TP_names)

# togliamo mestre
indices = lista_di_indici_senza_mestre_dalle_coordinate(cx, cy)
names_venezia = names_tot[indices]
coordsx = cx[indices]
coordsy = cy[indices]

# formattiamo l'array delle cordinate per poterlo salvare
coord_full = np.concatenate((coordsx, coordsy))
coord_full = np.reshape((coord_full), (2, np.round(coord_full.shape[0]/2).astype(int)))
coord_full = np.transpose(coord_full)
#plt.scatter(coord_full[:,0], coord_full[:,1])

# salvataggio
np.savetxt(folder + "/../txt/lista_key.txt", names_venezia, fmt='%s,')
np.savetxt(folder + "/../txt/lista_coords.txt", coord_full, fmt='%8.8f, %8.8f')

##### salva in pickle il gpd finale
import networkx as nt
import pickle

G = nt.read_shp(folder + "/../databases/stavolta_sono_giusto.shp")
G_un = G.to_undirected()

file = open('grafo_pickle', 'wb') 
pickle.dump(G_un, file)
file.close()




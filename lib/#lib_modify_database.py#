#questo script mi serve solo per selezionare le colonne che mi interessano del GeoDataFrame e salvarle in un nuovo file che contiene 2 strutture: indirizzo e coordinata; l'altra toponimo centroide . Inoltre deve salvare in numpy un array di nomi (sestieri e toponimi).

# una libreria per leggere gli shapefile --> info qui: http://geopandas.org/index.html
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

#from string import maketrans


def lista_di_indici_senza_mestre_dalle_coordinate(cx, cy):
    venezia_x = (cx > 2309038).astype(int) * (cx < 2314037).astype(int)
    venezia_y = (cy > 5033256).astype(int) * (cy < 5036386).astype(int)
    venezia = (venezia_x * venezia_y ).astype(bool)
    return venezia

folder = os.getcwd()

elstr_ponti = gpd.read_file(folder + "/pontiDivisi_completo" + "/pontiDivisi_completo.shp")
elstr_ponti.columns

civico = gpd.read_file(folder + "/data_bkp" + "/CIVICO.shp")
#streets_graph = gpd.read_file(folder + "/data" + "/EL_STR.shp")
TP = gpd.read_file(folder + "/../data_bkp" + "/TP_STR.shp")

TP_centroids = toponimi["geometry"].centroid
cx = [centroid.x if centroid else 0. for centroid in TP_centroids]
cy = [centroid.y if centroid else 0. for centroid in TP_centroids]
TP_names = toponimi["TP_STR_NOM"]

cx = np.asarray(cx)
cy = np.asarray(cy)

indices = lista_di_indici_senza_mestre_dalle_coordinate(cx, cy)

TP_names_venezia = TP_names[indices]
TP_centroids_venezia = TP_centroids[indices]

coordsx = cx[indices]
coordsy = cy[indices]

TP_coord_full = np.concatenate((coordsx, coordsy))
TP_coord_full = np.reshape((TP_coord_full), (2, np.round(TP_coord_full.shape[0]/2).astype(int)))

TP_coord_full = np.transpose(array_full)
plt.scatter(TP_coord_full[:,0], TP_coord_full[:,1])

np.savetxt(folder + "/lista_TP_csv.txt", TP_names_venezia, fmt='%s,')
np.savetxt(folder + "/lista_TP_coords_csv.txt", TP_coord_full, fmt='%8.8f, %8.8f')
#civico = gpd.read_file("/home/lucatastrophe/Desktop/venessia/Venessia4Working/data/Tema0301_ToponimiNumeriCivici/CIVICO.shp")

# trantab = {ord("0"):None,ord("1"):None,ord("2"):None,ord("3"):None,ord("4"):None,ord("5"):None,ord("6"):None,ord("7"):None,ord("8"):None,ord("9"):None,ord(","):None}
#
# indirizzi = civico["INDIRIZZO"].to_list()
# sestiere = []
# for ind in indirizzi:
#     if ind is None:
#          sestiere.append(None)
#      else:
#         sestiere.append(ind.translate(trantab))

new_civico_centroids = civico["geometry"].centroid
cx = [centroid.x if centroid else 0. for centroid in new_civico_centroids]
cy = [centroid.y if centroid else 0. for centroid in new_civico_centroids]
new_civico_names = civico["INDIRIZZO"]
new_civico_toponimo = civico["DENOMINAZI"]


assert(len(new_civico_names) == len(cx))

cx = np.asarray(cx)
cy = np.asarray(cy)

indices = lista_di_indici_senza_mestre_dalle_coordinate(cx, cy)

civici = new_civico_names[indices]
toponimi = new_civico_toponimo[indices]
print(toponimi)
coordsx = cx[indices]
coordsy = cy[indices]

lunghezza = elstr_ponti['geometry'].length
ponte = [1 if x else 0 for x in elstr_ponti["PONTE_TY"]]
new_ponti = gpd.GeoDataFrame(data = zip(elstr_ponti["geometry"],ponte, lunghezza), columns = ["geometry", "ponte", "length"])
new_civico = gpd.GeoDataFrame(data = zip(civico["CIVICO_NUM"], civico["INDIRIZZO"], civico["DENOMINAZI"], civico["geometry"]), columns = ["NUMERO", "INDIRIZZO", "TOPONIMO", "geometry"])coordsy = cy[indices]

array_full = np.concatenate((coordsx, coordsy))
array_full = np.reshape((array_full), (2, np.round(array_full.shape[0]/2).astype(int)))

array_t = np.transpose(array_full)
plt.scatter(array_t[:,0], array_t[:,1])

civici = [civico.replace(', ', ' ') if civico else "NOMEFALSO, 11" for civico in civici]
np.savetxt(folder + "/lista_civici_csv.txt", civici, fmt='%s,')
np.savetxt(folder + "/lista_toponimi_csv.txt", toponimi, fmt='%s,')
np.savetxt(folder + "/lista_coords_csv.txt", array_t, fmt='%8.8f, %8.8f')

#####

new_civico_only_names_and_centroids = []
for i in range(len(new_civico_centroids_without_nones)):
    new_civico_only_names_and_centroids.append((new_civico_names[i], cx[i], cy[i]))

# TEST
civici_full = np.asarray(new_civico_only_names_and_centroids)
testlist = civici_full[:,1:3]
centroids_as_points = [(centroid[0], centroid[1]) for centroid in testlist]
centroids_as_points_in_array = np.ascontiguousarray(centroids_as_points)
centroids_as_points_in_array.flags
centroids_as_points_in_array[:,0] > 0
c_res = np.reshape(centroids_as_points_in_array[:,0], centroids_as_points_in_array.shape[0])

print(c_res.ndim)
arrayrandom = np.zeros(3)
print(arrayrandom.ndim)
arrayrandom > 0
c_res > 0
c_res.flags
arrayrandom.flags
venezia_x = c_res[:] > 2309038




centroids = testlist[:,1:3]
centroids_as_points = [(centroid[0], centroid[1]) for centroid in centroids]
centroids_as_points_in_array = np.asarray(centroids_as_points)
len(testlist)
testlist1array = float(testlist1array)
new_civico_names[10]
lista_civici_full = []
lista_civici_full.append(new_civico_names)
lista_civici_full.append(new_civico_centroids_without_nones)
np.asarray(lista_civici_full[1])
# TOPLEFT: 2309038, 5036386
# BOTTOMRIGHT: 2314037, 5033256
def elimina_mestre_da_lista(lista):
    centroids = lista[:,1:3]
    centroids_as_points = [(centroid[0], centroid[1]) for centroid in centroids]
    centroids_as_points_in_array = np.asarray(centroids_as_points)
    venezia = np.zeros(centroids_as_points_in_array.shape[0], dtype='bool')
    for i in range(centroids_as_points_in_array.shape[0]):
        venezia_x = (float(centroids_as_points_in_array[i,0]) > 2309038) * (float(centroids_as_points_in_array[i,0]) < 2314037)
        venezia_y = (float(centroids_as_points_in_array[i,1]) > 5033256) * (float(centroids_as_points_in_array[i,1]) < 5036386)
        venezia[i] = (venezia_x * venezia_y )

    return lista[venezia,:]

lista_civici_venezia = elimina_mestre_da_lista(civici_full)

|# TOPLEFT: 2309038, 5036386
# BOTTOMRIGHT: 2314037, 5033256
def elimina_mestre(shp_to_clean):
    centroids = shp_to_clean["geometry"].centroid
    centroids_as_points = [(centroid.x, centroid.y) for centroid in centroids]
    centroids_as_points_in_array = np.asarray(centroids_as_points)
    venezia_x = (centroids_as_points_in_array[:,0] > 2309038).astype(int) * (centroids_as_points_in_array[:,0] < 2314037).astype(int)
    venezia_y = (centroids_as_points_in_array[:,1] > 5033256).astype(int) * (centroids_as_points_in_array[:,1] < 5036386).astype(int)
    venezia = (venezia_x * venezia_y ).astype(bool)
    venezia
    return shp_to_clean[venezia]

ponti_a_venezia = elimina_mestre(new_ponti)
civico_venezia = elimina_mestre(new_civico)
len(ponti_a_venezia)
len(civico_venezia)
ponti_a_venezia.plot()
#new_ponti.to_file(folder + "/pontiDivisi_completo" + "/pontiDivisi_modificato.shp")
ponti_a_venezia.to_file(folder + "/pontiDivisi_completo" + "/pontiDivisi_solo_venezia_l.shp")
ponti_a_venezia.to_file(folder + "/pontiDivisi_completo" + "/pontiDivisi_solo_venezia_l.shp")

#total = gpd.GeoDataFrame(data = zip(civico["CIVICO_NUM"], sestiere, civico["DENOMINAZI"], civico["geometry"]),lunghezza, ponte, columns = ["NUMERO", "SESTIERE", "TOPONIMO", "geometry", "lunghezza", "ponte"])
#venezia_ind  = total["SESTIERE"].str.contains( "DORSODURO|CANNAREGIO|SAN POLO|^SAN MARCO|SANTA CROCE|CASTELLO") #aggiungere isole
#total.index = venezia_ind
#venezia = total.loc[True]

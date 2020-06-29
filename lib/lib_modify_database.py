# Per creare il grafo per il sito e i txt con i nomi e le coordinate: - su qgis, convertire in epsg4326 tutti gli shp -civico.shp, EL_STR, TP_STR - (apro civico.shp -l'originale- al dialogo iniziale gli dico di usare epgs3004 -perché così vanno interpretate le sue coordinate- una volta caricata la mappa vado su layer-> "save layer as" e lì gli indico il crs epsg4326), spezzare i ponti (chissà come, ale lo sa) - da questo script, togliere mestre, togliere le colonne inutili, salvare in pickle e aggiornare il txt

import geopandas as gpd
# per i grafici
import matplotlib.pyplot as plt
# per il debug
import pdb
import numpy as np
# per le cartelle
import os

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

EPSG3004_Venezia = 'PROJCS["unnamed",GEOGCS["International 1909 (Hayford)",DATUM["unknown",SPHEROID["intl",6378388,297],TOWGS84[-130.5633,-29.2694,-6.12,-1.05572,-2.6951,-2.28808,-16.9352]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["latitude_of_origin",0],PARAMETER["central_meridian",15],PARAMETER["scale_factor",0.9996],PARAMETER["false_easting",2520000],PARAMETER["false_northing",0],UNIT["Meter",1]]'

TP = TP.to_crs(EPSG3004_Venezia)
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

names_venezia = [civico.replace(', ', ' ') if civico else "NOMEFALSO, 11" for civico in names_venezia]
# salvataggio
np.savetxt(folder + "/../txt/lista_key.txt", names_venezia, fmt='%s,')
np.savetxt(folder + "/../txt/lista_coords.txt", coord_full, fmt='%8.8f, %8.8f')

#%% Import graph land
##### salva in pickle il gpd finale (strade). SHP deve già essere om WSG4
import geopandas as gpd
import networkx as nt
import pickle
from lib_func_import import lines_length
import os

folder = os.getcwd()
# il file shp è stato creato in epsg3004 ma convertito in epsg4326 utilizzando conversione standard
shp_land = "/../databases/venezia_isole_ponti_civici_4326VE.shp"
streets = gpd.read_file(folder + shp_land)
# # riconvertiamo a 3004
#
# streets = streets.to_crs(epsg=3004)
# # convertiamo alle coordinate modificate ottimizzate per venezia
# streets = streets.to_crs(EPSG3004_Venezia)
# lunghezza = streets['geometry'].length

# calcola lunghezze delle linestring utilizzando un metodo bello
lunghezza = lines_length(streets['geometry'])
ponte=[]
for bridge in streets["PONTE_CP"]:
    ponte.append(1 if bridge=="02" else 0)
# crea nuovo dataframe con solo colonne interessanti
total = gpd.GeoDataFrame(data = zip(lunghezza, ponte, streets["geometry"],streets['CVE_SUB_CO'],streets['VEL_MAX']), columns = ["length","ponte", "geometry","street_id","vel_max"])
# salva nuovo dataframe in shp
new_shp_name = "/../databases/venezia_isole_ponti_civici_4326VE_gpd.shp"
total.to_file(folder + new_shp_name)

# ricarica lo shapefile in networkx come grafo
G = nt.read_shp(folder + new_shp_name)
# rendi grafo undirected
G_un = G.to_undirected()

# salva il grafo come pickle
pickle_name = "/../databases/grafo_pickle_4326VE"
with open(folder+pickle_name, 'wb') as file:
    pickle.dump(G_un, file)

#%% Import graph water

##### salva in pickle il gpd finale (acqua). SHP deve già essere om WSG4
shp_water = "/../databases/acqua_WGS_4326VE.shp"
acqua = gpd.read_file(folder + shp_water)
# calcola lunghezze linestring
lunghezza = lines_length(acqua['geometry'])
vel_max=acqua['VEL_MAX']
solo_remi=[1 if i=='Rio Blu' else 0 for i in acqua['BARCHE_A_R']]
# normativa: to be done
# c'è anche la stazza, ma per il momento non ci interessa (10t)
larghezza=acqua['LARGHEZZA_']
senso_unico=acqua['ONEWAY']
total = gpd.GeoDataFrame(data = zip(lunghezza, vel_max, solo_remi, larghezza, senso_unico, acqua["geometry"]), columns = ["length","vel_max", "solo_remi", "larghezza", "senso_unico", "geometry"])
new_shp_name = "/../databases/acqua_WGS_4326VE_gpd.shp"
total.to_file(folder + new_shp_name)


G = nt.read_shp(folder + new_shp_name)
G_un = G.to_undirected()
pickle_name = "/../databases/grafo_acqueo_pickle_4326VE"
with open(folder+pickle_name, 'wb') as file:
    pickle.dump(G_un, file)

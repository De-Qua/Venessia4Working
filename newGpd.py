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

#from string import maketrans


folder = os.getcwd()
elstr_ponti = gpd.read_file(folder + "/pontiDivisi_completo" + "/pontiDivisi_completo.shp")
elstr_point.columns
streets_graph = gpd.read_file(folder + "/data" + "/EL_STR.shp")
streets_names = gpd.read_file(folder + "/data" + "/TP_STR.shp")
civico = gpd.read_file("/home/lucatastrophe/Desktop/venessia/Venessia4Working/data/Tema0301_ToponimiNumeriCivici/CIVICO.shp")

#trantab = {ord("0"):None,ord("1"):None,ord("2"):None,ord("3"):None,ord("4"):None,ord("5"):None,ord("6"):None,ord("7"):None,ord("8"):None,ord("9"):None,ord(","):None}

indirizzi = civico["INDIRIZZO"].to_list()
sestiere = []
for ind in indirizzi:
    if ind is None:
        sestiere.append(None)
    else:
        sestiere.append(ind.translate(trantab))

new_ponti = gpd.GeoDataFrame(data = zip(elstr_ponti["geometry"],elstr_ponti["PONTE_TY"]), columns = ["geometry", "ponte"])
new_ponti.to_file(folder + "/pontiDivisi_completo" + "/pontiDivisi_modificato.shp")

#total = gpd.GeoDataFrame(data = zip(civico["CIVICO_NUM"], sestiere, civico["DENOMINAZI"], civico["geometry"]),lunghezza, ponte, columns = ["NUMERO", "SESTIERE", "TOPONIMO", "geometry", "lunghezza", "ponte"])
#venezia_ind  = total["SESTIERE"].str.contains( "DORSODURO|CANNAREGIO|SAN POLO|^SAN MARCO|SANTA CROCE|CASTELLO") #aggiungere isole
#total.index = venezia_ind
#venezia = total.loc[True]

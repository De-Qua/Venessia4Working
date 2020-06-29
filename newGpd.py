#questo script mi serve solo per selezionare le colonne che mi interessano del GeoDataFrame e salvarle in un nuovo shapefile. Inoltre deve salvare in numpy un array di nomi unici (sestieri e toponimi)

# una libreria per leggere gli shapefile --> info qui: http://geopandas.org/index.html
import geopandas as gpd
# per i grafici
import matplotlib.pyplot as plt
# per il debug
import pdb
# per le cartelle
import os
# metodo per avere gli indici delle vie o della via trovata

folder = os.getcwd()
#streets_graph = gpd.read_file(folder + "/data" + "/EL_STR.shp")
#streets_names = gpd.read_file(folder + "/data" + "/TP_STR.shp")
civico = gpd.read_file("data_bkp/CIVICO_4326.shp")

civico.columns
civico['DENOMINAZI'].head()
civico['DENOMINA_1'].head()
civico['INDIRIZZO'].head()

trantab = {ord("0"):None,ord("1"):None,ord("2"):None,ord("3"):None,ord("4"):None,ord("5"):None,ord("6"):None,ord("7"):None,ord("8"):None,ord("9"):None,ord(","):None}

indirizzi = civico["INDIRIZZO"].to_list()
sestiere = []
for ind in indirizzi:
    if ind is None:
        sestiere.append(None)
    else:
        sestiere.append(ind.translate(trantab))

total = gpd.GeoDataFrame(data = zip(civico["CIVICO_NUM"], sestiere, civico["DENOMINAZI"], civico["geometry"]), columns = ["NUMERO","SESTIERE", "TOPONIMO", "geometry"])
venezia_ind  = total["SESTIERE"].str.contains( "DORSODURO|CANNAREGIO|SAN POLO|^SAN MARCO|SANTA CROCE|CASTELLO")
total.index = venezia_ind
venezia = total.loc[True]

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


folder = os.getcwd()
streets_graph = gpd.read_file(folder + "/data" + "/EL_STR.shp")
streets_names = gpd.read_file(folder + "/data" + "/TP_STR.shp")
civico = gpd.read_file(folder + "/data" + "/CIVICO.shp")

# scrive sulla console il contenuto del file
#print(streets_graph)
#print(streets_names)

pdb.set_trace()
#streets_list = streets_names["TP_STR_NOM"].tolist()
streets_list = civico["DENOMINAZI"].tolist()
# removing one (or more) annoying none values
streets_corrected = [street if street else "" for street in streets_list]

starting_address = input('Da dove parti?\n')

matches = get_close_matches_indexes(starting_address.upper(), streets_corrected)
#pdb.set_trace()
streets_founds = []
for i in range(len(matches)):
    streets_founds.append(streets_list[matches[i]])
    print("Trovato: {}:{}".format(i, streets_founds[i]))
which_one = int(input("Quale intendi? Scrivi il numero\n"))

#pdb.set_trace()
streets_coordinates1 = streets_names['CVE_COD_VI']
streets_coordinates2 = streets_names['CVE_SCOD_V']
#streets_coordinates = [streets_coordinates1, streets_coordinates2]
coordinates = [streets_coordinates1[matches[which_one]], streets_coordinates2[matches[which_one]]]

print("si trova a {}, {}".format(coordinates[0], coordinates[1]))



# # mostra la mappa (serve il plt.show())
# streets_graph.plot()
# streets_names.plot()
# plt.show()

#blocca il debug
pdb.set_trace()


# test con il shapefile..
#shapefile.cx
#shapefile.crs
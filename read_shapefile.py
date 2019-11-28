# una libreria per leggere gli shapefile --> info qui: http://geopandas.org/index.html
import geopandas as gpd
# per i grafici
import matplotlib.pyplot as plt
# per il debug
import pdb
# per le cartelle
import os



folder = os.getcwd()
shapefile = gpd.read_file(folder + "/data" + "/CV_LIV.shp")
# scrive sulla console il contenuto del file
print(shapefile)

# mostra la mappa (serve il plt.show())
shapefile.plot()
plt.show()

#blocca il debug
#pdb.set_trace()

# test con il shapefile..
#shapefile.cx
#shapefile.crs
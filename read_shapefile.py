# una libreria per leggere gli shapefile --> info qui: http://geopandas.org/index.html
import geopandas as gpd
import pdb

folder = "/Users/Palma/Documents/Projects/Venessia4Working/Data/20191113_DBGT_SHP"
strato = "/Strato05_Orografia"
tema = "/Tema0501_Altimetria"
shapefile = gpd.read_file(folder + strato + tema + "/CV_LIV.shp")
# scrive sulla console il contenuto del file
print(shapefile)
#blocca il debug qui per testare cosa si puo fare
pdb.set_trace()
# dovrebbe plottare il tutto ma non lo fa
shapefile.plot()

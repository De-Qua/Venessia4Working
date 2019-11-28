import geopandas as gpd
import pdb

folder = "/Users/Palma/Documents/Projects/Venessia4Working/Data/20191113_DBGT_SHP"
strato = "/Strato05_Orografia"
tema = "/Tema0501_Altimetria"
shapefile = gpd.read_file(folder + strato + tema + "/CV_LIV.shp")
pdb.set_trace()
print(shapefile)
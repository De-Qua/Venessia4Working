


small_shp = gpd.read_file("/home/lucatastrophe/Desktop/Intersezioni/QUARTIERE.shp")


lunghezza = small_shp['geometry'].length
ponte = [1 if x else 0 for x in small_shp["PONTE_TY"]]
total = gpd.GeoDataFrame(data = zip(lunghezza, ponte, small_shp["geometry"]), columns = ["length","ponte", "geometry"])

#ponti = (total["ponte"] == 1)
#total.index = ponti
#new = total.loc[True]

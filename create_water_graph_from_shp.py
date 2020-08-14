
##### salva in pickle il gpd finale (strade). SHP deve già essere om WSG4
import geopandas as gpd
import networkx as nt
import pickle
from lib.lib_func_import import lines_length
import os
import sys
import datetime

if __name__ == "__main__":

    print("\n******************************************")
    print(" ### WATER VERSION ###")
    print("Let's create a networkx graph from a shp file!\nI hope you gave as a parameter the shp file or hard-coded in the text! :)")
    print("Either pass as parameter: python3 shp_path (full, not relative)\nor write the folder at line 16 and the name at line 22 :)")
    print("******************************************\n")

    folder = "/Users/Palma/Documents/Projects/Venessia4Working/Venessia4Working/data" #os.getcwd()

    if len(sys.argv) > 1:
        print("great, path is gien as {}\nThanks".format(sys.argv[1]))
        shp_path = sys.argv[1]
    else:
        shp_relative_path = "dequa_ve_acqua_v4.shp"
        shp_path = os.path.join(folder, shp_relative_path)
        print("no path given, we use hard-coded one, which now is: {}".format(shp_path))

    print("reading the file..")
    shp_gpd = gpd.read_file(shp_path)

    print("adapting to our needs..")
    lunghezza = lines_length(shp_gpd['geometry'])
    solo_remi=[1 if i=='Rio Blu' else 0 for i in shp_gpd['BARCHE_A_R']]
    # normativa: to be done
    # c'è anche la stazza, ma per il momento non ci interessa (10t)
    vel_max=shp_gpd['VEL_MAX']
    larghezza=shp_gpd['LARGHEZZA_']
    senso_unico=shp_gpd['ONEWAY']

    print("creating a new dataframe only with the data we need..")
    # crea nuovo dataframe con solo colonne interessanti
    total = gpd.GeoDataFrame(data = zip(lunghezza, vel_max, solo_remi, larghezza, senso_unico, shp_gpd["geometry"]), columns = ["length","vel_max", "solo_remi", "larghezza", "senso_unico", "geometry"])

    today = datetime.datetime.today().strftime ('%d%m')

    print("saving the adapted version as the name plus suffix _dequa_{today} to understand..")# salva nuovo dataframe in shp
    new_shp_name = "{}_dequa_ve_acqua_{}.shp".format(shp_path[:-4], today)
    total.to_file(new_shp_name)

    print("now create the graph with networkx..")
    # ricarica lo shapefile in networkx come grafo
    G = nt.read_shp(new_shp_name)
    # rendi grafo undirected
    G_un = G.to_undirected()

    print("cool, if we got here, everything worked! Now we can pickle the graph..")
    # salva il grafo come pickle
    pickle_name = "{}_pickle_4326VE".format(new_shp_name)
    with open(pickle_name, 'wb') as file:
        pickle.dump(G_un, file)

    print("PPUUUUUUUUUUUUUUUUMMMMMM!")

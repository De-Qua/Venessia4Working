##### salva in pickle il gpd finale (strade). SHP deve già essere om WSG4
import geopandas as gpd
import networkx as nt
import pickle
from lib.lib_func_import import lines_length
import os
import sys
import datetime
import pdb

if __name__ == "__main__":

    print("\n******************************************")
    print(" ### LAND VERSION ###")
    print("Let's create a networkx graph from a shp file!\nI hope you gave as a parameter the shp file or hard-coded in the text! :)")
    print("Either pass as parameter: python3 shp_path (full, not relative)\nor write the folder at line 16 and the name at line 22 :)")
    print("******************************************\n")

    folder = "/Users/ale/Documents/Venezia/MappaDisabili/data/OpenDataVenezia/dequa_ve_shp/terra" #os.getcwd()
    shp_relative_path = "v8/dequa_ve_terra_v8.shp"

    if len(sys.argv) > 1:
        print("great, path is given as {}\nThanks".format(sys.argv[1]))
        #shp_path = os.path.join(sys.argv[1], shp_relative_path)
        shp_path = sys.argv[1]
    else:

        shp_path = os.path.join(folder, shp_relative_path)
        print("no path given, we use hard-coded one, which now is: {}".format(shp_path))

    print("reading the file..")
    streets = gpd.read_file(shp_path)

    print("adapting to our needs..")
    lunghezza = lines_length(streets['geometry'])

    list_of_Codice_Pon_flat = ["MELONI"]
    # L'elenco di questi ponti è preso da https://www.comune.venezia.it/it/content/venezia-accessibile-itinerari-senza-barriere
    list_of_Codice_Pon_gradino_agevolato = ["PAGLIA", "SECHER", "PIERO", "RASPI", "GUGLIE", "PAPADO"]
    list_of_Codice_Pon_gradino_agevolato_con_accomp = ["FELICE"]
    list_of_Codice_Pon_rampa_fissa = ["QUINTA", "PALUDO"]
    list_of_Codice_Pon_rampa_provvisoria_feb_nov = ["VIN"]
    list_of_Codice_Pon_rampa_provvisoria_set_giu = ["MOLIN", "SALUTE", "CABALA", "INCURA", "CALCINA", "LUNGO"]
    list_of_Codice_Pon_rampa_provvisoria_mag_nov = ["VENETA"]

    ponte = []
    accessible = []
    for bridge in streets["Codice_Pon"]:
        if bridge:
            if bridge in list_of_Codice_Pon_flat:
                ponte.append(0)
                accessible.append(1)
            elif bridge in list_of_Codice_Pon_gradino_agevolato:
                ponte.append(1)
                accessible.append(2)
            elif bridge in list_of_Codice_Pon_gradino_agevolato_con_accomp:
                ponte.append(1)
                accessible.append(3)
            elif bridge in list_of_Codice_Pon_rampa_fissa:
                ponte.append(1)
                accessible.append(4)
            elif bridge in list_of_Codice_Pon_rampa_provvisoria_feb_nov:
                ponte.append(1)
                accessible.append(5)
            elif bridge in list_of_Codice_Pon_rampa_provvisoria_set_giu:
                ponte.append(1)
                accessible.append(6)
            elif bridge in list_of_Codice_Pon_rampa_provvisoria_mag_nov:
                ponte.append(1)
                accessible.append(7)
            else:
                ponte.append(1)
                accessible.append(0)
        else:
            ponte.append(0)
            accessible.append(1)

    print("creating a new dataframe only with the data we need..")
    # crea nuovo dataframe con solo colonne interessanti
    # pdb.set_trace()
    total = gpd.GeoDataFrame(data=zip(lunghezza, ponte, accessible,
                                      streets["geometry"], streets['V4W_ID'], streets['VEL_MAX'],
                                      streets['max_tide'], streets['min_tide'], streets['avg_tide'], streets['med_tide'],
                                      streets['Pass_cmZPS'], streets['Pass_altez']),
                             columns=["length", "ponte", "accessible",
                                      "geometry", "street_id",
                                      "vel_max", "max_tide", "min_tide", "avg_tide", "med_tide",
                                      "passerelle_cm_zps", "passerrelle_height"])

    today = datetime.datetime.today().strftime('%d%m')

    print("saving the adapted version as the name plus suffix _{today} to understand..")  # salva nuovo dataframe in shp
    new_shp_name = "{}_{}.shp".format(shp_path[:-4], today)
    total.to_file(new_shp_name)

    print("now create the graph with networkx..")
    # ricarica lo shapefile in networkx come grafo
    G = nt.read_shp(new_shp_name)
    # rendi grafo undirected
    G_un = G.to_undirected()

    print("cool, if we got here, everything worked! Now we can pickle the graph..")
    # salva il grafo come pickle
    pickle_name = "{}_pickle_4326VE".format(new_shp_name[:-4])
    with open(pickle_name, 'wb') as file:
        pickle.dump(G_un, file)

    print("PPUUUUUUUUUUUUUUUUMMMMMM!")

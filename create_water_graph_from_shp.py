
##### salva in pickle il gpd finale (strade). SHP deve già essere om WSG4
import geopandas as gpd
import networkx as nt
import numpy as np
import pickle
import csv
from lib.lib_func_import import lines_length
import os
import sys
import datetime
import pdb
import pandas as pd

if __name__ == "__main__":

    print("\n******************************************")
    print(" ### WATER VERSION ###")
    print("Let's create a networkx graph from a shp file!\nI hope you gave as a parameter the shp files or hard-coded in the text! :)")
    print("Either pass as parameter: python3 shp_path (full, not relative)\nor write the folder at line 16 and the name at line 22 :)")
    print("******************************************\n")

    folder = os.getcwd()
#    "/Users/Palma/Documents/Projects/Venessia4Working/Venessia4Working/data" 
    shp_relative_path = "dequa_ve_acqua_v7.shp"
    zucchetta_relative_path = "Final Ponti Data CSV.csv"
    ponti = []

    if len(sys.argv) > 2:
        shp_path = sys.argv[1]
        zucchetta_path = sys.argv[2]
        print("great, path is given as {}\nzucchetta is given as {}\nThanks".format(shp_path,zucchetta_path))
    elif len(sys.argv) > 1:
        shp_path = sys.argv[1]
        zucchetta_path = os.path.join(folder, zucchetta_relative_path)
        print("great, path is given as {}\nno zucchetta is given, we use hard-coded one, which now is: Thanks".format(sys.argv[1], zucchetta_path))
    else:
        shp_path = os.path.join(folder, shp_relative_path)
        zucchetta_path = os.path.join(folder, zucchetta_relative_path)
        print("no path given, we use hard-coded one, which for shp is: {}\nfor zucchetta is: {}".format(shp_path, zucchetta_path))

    print("\n\n\n\n\n*****\nWARNING\nCONTROLLA I PONTI! DA ZUCCHETTA A COMUNE\n*****\n\n\n\n\n")
    with open(zucchetta_path, 'r', encoding='latin') as csvfile:
        reader = csv.reader(csvfile)
        first_row = True
        for row in reader:
            if first_row:
                col_num_as_list = [i for i in range(len(row)) if row[i] == 'Minimum Height (m)']
                first_row = False
                col_num = col_num_as_list[0]
            elif row[0]:
                ponti.append({'altezza':row[col_num], 'bridge_num_zucchetta':row[0], 'nome':row[1]})
    print("reading the file..")
    shp_gpd = gpd.read_file(shp_path)

    print("adapting to our needs..")
    lunghezza = lines_length(shp_gpd['geometry'])
    solo_remi=[1 if i=='Rio Blu' else 0 for i in shp_gpd['BARCHE_A_R']]
    # normativa: to be done
    # c'è anche la stazza, ma per il momento non ci interessa (10t)
    vel_max=shp_gpd['VEL_MAX'][:]
    vel_max_mp=shp_gpd['VEL_MAX_MP'][:]
    larghezza=shp_gpd['LARGHEZZA_']
    senso_unico=shp_gpd['ONEWAY'][:]
    orario_senso_start=gpd.GeoSeries(np.zeros([larghezza.size], dtype=np.int8))
    orario_senso_end=gpd.GeoSeries(np.ones([larghezza.size], dtype=np.int8)*24)
    orario_chiuso_start=gpd.GeoSeries(np.ones([larghezza.size], dtype=np.int8)*24)
    orario_chiuso_end=gpd.GeoSeries(np.ones([larghezza.size], dtype=np.int8)*24)
    altezza=np.double(np.ones_like(solo_remi))*1000

    lista_sensi_inversi=["DE SAN LUCA - ROSSINI", "DE PALAZZO - CANONICA", "DE LA FAVA","DE LA PIETA'  - SANT'ANTONIN","DE SAN GIUSEPPE", "DE LA TETA - SAN GIOVANNI LATERANO RAMO BASSO", "DE SAN GIACOMO DALL'ORIO","DE SAN VIO"]
    lista_limiti_sette=["GRANDE","DE CANNAREGIO"]

    lista_no_info_per_non_dimenticare=["DE LE GALEAZZE", "SCUOLA GABELLI","DE LA VERONA - MENUO" ]
    lista_limiti_laguna=["DE LA RANA", "MOLO B", "DI CAMPALTO","COA DI LATTE","MORTO - MAZZORBO","CARBONERA","ALTINO","MONTIRON","DE SANT'ANTONIO","DEL COLPO", "DI BOSSOLARO", "LA ROTTA","CAMPANA", "BOMBAE", "PORTOSECCO","DE LA CAVA","CODA REZIOL"]
    vel_laguna=10
    lista_limiti_centro=["SCUOLA GABELLI","A. CANAL","DE LA SACA DE LA MISERICORDIA","ARSENAL VECHIO"] # in realtà sono quasi tutti al lido
    lista_divieti_0_24 = ["ARSENAL VECHIO"]################## caso particolare, gli altri hanno il divieto di transito nella colonna giusta!
    # canali con limite per canoe e simili dalle 8 alle 15 lunedì-venerdì e dalle 8 alle 13 il sabato
    lista_no_remetti = ["Canal Grande", "Cannaregio", "Giardini", "Greci - San Lorenzo", "- Santa Giustina - Sant’Antonin – Pietà", "Noale", "Novo", "Ca’ Foscari", "Santi Apostoli - Gesuiti"] # nomi da correggere
    vel_centro=5
    ponte_codes_list=[]
    epsilon=0.001
    for index,canal in shp_gpd.iterrows():

        print(canal['TC_DENOM'])
        if canal['DIVIETO_TR']:
            if 'art. 8' in canal['DIVIETO_TR']:
                print('divieto transito imbarcazioni a motore, esclusi concessionari spazi acquei e unità di enti e aziende pubbliche')
                orario_chiuso_start[index]=0
        if canal['DIVdiporto']:    
            print(canal['DIVdiporto'])
            orario_chiuso_start[index]=8
            orario_chiuso_end[index]=12
            
        if canal['VEL_MAX']==0:
            print(' has max vel=0')
            if canal['TC_DENOM'] in lista_limiti_laguna:
                vel_max[index]=vel_laguna
            if canal['TC_DENOM'] in lista_limiti_centro:
                vel_max[index]=vel_centro
            if not canal['TC_DENOM']:
                print("changed max speed in none canal")
                vel_max[index]=vel_laguna
        if canal['VEL_MAX_MP']==0:
           # print(canal['TC_DENOM'], ' has max vel=0')
            if canal['TC_DENOM'] in lista_limiti_laguna:
                vel_max_mp[index]=vel_laguna
            if canal['TC_DENOM'] in lista_limiti_centro:
                vel_max_mp[index]=vel_centro
            if not canal['TC_DENOM']:
                vel_max_mp[index]=vel_laguna
                
        if solo_remi[index]==1:
            #print('era un rio blu')
            vel_max_mp[index]=vel_centro
            vel_max[index]=vel_centro
    
        if not np.isnan(canal['Numero_Zuc']): # != "None": #is not None:
            print('trovato ponte ', canal['Nome_Ponte'])
            for ponte in ponti:

                if np.abs(float(ponte['bridge_num_zucchetta'])-float(canal['Numero_Zuc']))<epsilon:
                    ponte_codes_list.append(canal['Numero_Zuc'])
                    altezza[index]=ponte['altezza']
                    print("il ponte {} e alto {}".format(ponte['nome'], ponte['altezza']))
                    break
        if canal['TC_DENOM']=="DEI FUSERI":
            print('aggiungo senso unico al rio dei fuseri')
            senso_unico[index]=1
        if canal['TC_DENOM']=="DEI VETRAI":
            print('aggiungo senso unico al rio dei vetrai')
            senso_unico[index]=1
        if canal['TC_DENOM']=="DE CA' FOSCARI":
            print('aggiungo senso unico al rio di ca foscari')
            senso_unico[index]=1
        if senso_unico[index] is not None:

            if canal['TC_DENOM'] in lista_sensi_inversi:
                print('cambiato verso di ', canal['TC_DENOM'])
                senso_unico[index]=-1
            else:
                senso_unico[index]=1
            if canal['TC_DENOM'] in ["DE CA' FOSCARI", "NOVO"]:
                orario_senso_start[index]=0
                orario_senso_end[index]=12
            if canal['TC_DENOM']=="DEI VETRAI":
                orario_senso_start[index]=8 #solo feriali
                orario_senso_end[index]=14

        if canal['TC_DENOM'] in lista_limiti_sette:
            print('cambio limite di velocita nel ', canal['TC_DENOM'])
            vel_max[index]=7
            vel_max_mp[index]=11
        if canal['TC_DENOM']=="SAN CRISTOFORO":
            print('modifico limite di velocita canale di san cristoforo')
            vel_max[index]=11

    assert(len(ponti)==len(ponte_codes_list),'diversi ponti tra shp e csv')

    #da aggiungere a total: h_closed_start, h_closed_end
    total = gpd.GeoDataFrame(data = zip(lunghezza, vel_max, vel_max_mp, solo_remi, larghezza, altezza, senso_unico, orario_senso_start,orario_senso_end, orario_chiuso_start, orario_chiuso_end, shp_gpd["TC_DENOM"],shp_gpd["geometry"]),
    columns = ["length","vel_max", "vel_max_mp", "solo_remi", "larghezza", "altezza", "senso_unico", "h_su_start","h_su_end", "dt_start", "dt_end", "nome","geometry"])

    today = datetime.datetime.today().strftime ('%d%m')

    print("saving the adapted version as the name plus suffix _dequa_{today} to understand..")# salva nuovo dataframe in shp
    new_shp_name = "{}/{}_{}.shp".format(shp_path[:],shp_relative_path[:-4] ,today)
    total.to_file(new_shp_name)

    print("now create the graph with networkx, from file: ", new_shp_name)
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

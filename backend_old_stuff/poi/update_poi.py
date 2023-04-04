import os
print(os.getcwd())
import backend_old_stuff.poi.library_overpass as lib_over
import pdb

pdb.set_trace()
bbox_venezia = [45.36, 12.32, 45.47, 12.41]
osm_id_venezia = 44741
# doppie virgolette servono!
only_amenity = [
    "'amenity'"
    ]
#filters = ["'operator'='ACTV'"]
what_we_get = lib_over.download_data(osm_id_venezia, [], what='all')

len(what_we_get['elements'])
what_we_get.keys()
what_we_get['elements'][0]

import json
with open('backend_old_stuff/poi/poi_search.json', 'r') as ps:
    pois_dd = json.load(ps)

pois_dd.keys()
len(pois_dd['elements'])
lib_over.draw_the_data(what_we_get, 'our search drawn on a map')
lib_over.save_data_as(what_we_get, 'backend_old_stuff/poi/poi_amenity.json')
everything = lib_over.download_data(osm_id_venezia, [], what='all')
len(everything['elements'])

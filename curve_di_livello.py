##### salva in pickle il gpd finale (strade). SHP deve già essere om WSG4
import geopandas as gpd
import networkx as nt
import pickle
import os
import sys
import datetime
import pdb
import shapely.wkt as wkt
import numpy as np
#%%
cl_folder = "/Users/ale/Downloads/curve_livello_polyline_4326VE_proj"
# cl_path = os.path.join(cl_folder, "curve_livello_polyline_4326VE_proj.shp")
cl_path = os.path.join(cl_folder, "curve_livello_polyline_4326VE_proj_V4Wid_ok.shp")
curve_di_livello = gpd.read_file(cl_path)
#curve_di_livello['geometry'][0]
geom_curves = curve_di_livello['geometry']
curve_di_livello_4326 = curve_di_livello.to_crs(4326)
#archi
archi_folder = '/Users/ale/Downloads/v11'
archi_path = os.path.join(archi_folder, "dequa_ve_terra_v11.shp")
archi = gpd.read_file(archi_path)

gpd.io.file.infer_schema(archi)
archi.schema

#envelope per shapely
envelope_folder = '/Users/ale/Downloads/TP_STR'
envelope_path = os.path.join(envelope_folder, "TP_STR_v2")
envelopes = gpd.read_file(envelope_path)

# path_graph = os.path.join(folder, 'dequa_ve_terra_v8_dequa_ve_terra_0509_pickle_4326VE')
# with open(path_graph, 'rb') as file:
#     G_un = pickle.load(file)
#%%
import shapely
print(shapely.__version__)
from shapely.ops import voronoi_diagram
import geopandas as gpd
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from shapely.ops import voronoi_diagram as svd
from shapely.geometry import Polygon, MultiPolygon

list_of_altitudes=np.linspace(80, 200,1)
#%%
i=0
err = 0
for geom_polygon, polygon_id in envelopes[['geometry','V4W_ID']].values:
    if polygon_id == 0: # alcuni poligoni hanno 0 e questo crea casini perché anche non è univoco…
        continue
    # i = i+1
    # if i > 100:
    #     break
    print(f"*** Working with polygon: {polygon_id}")
    edges = archi[archi['V4W_ID']==polygon_id]
    if edges.empty:
        print(f'Edges in {polygon_id} empty')
        continue
    geom_edges = edges['geometry']
    edge_scaled = geom_edges.scale(xfact=0.9, yfact=0.9)
    edge_dataframe = gpd.GeoDataFrame(geometry=edge_scaled, crs=4326).reset_index(drop=True)
    # edge_buffer = bufferDissolve(edge_dataframe,10e-10)
    # edge_dataframe.buffer(10e-10)
    edge_in_polygon = edge_dataframe
    #edge_in_polygon = edge_dataframe[~edge_dataframe.disjoint(geom_polygon)].reset_index(drop=True)
    edge_in_polygon['edge_id'] = edge_in_polygon.index
    try:
        vd = voronoiDiagram4plg(edge_in_polygon, geom_polygon)
    except:
        print("Topologic error in voronoi diagram")
        err = err+1
        continue
    vd['voronoi_id'] = vd.index
    # edge_in_polygon.to_file(f'edges.geojson', driver= "GeoJSON")
    # edge_dataframe.to_file(f'edges_df.geojson', driver= "GeoJSON")
    # vd.to_file(f'output_{i}.geojson', driver='GeoJSON')
    # print('File created')
    # #interseca i singoli poligoni all'interno di un vd con le curve di livello
    # for ind in range(len(vd)):

    #curve_nel_vd = curve_di_livello_4326[curve_di_livello_4326.intersects(vd['geometry'][ind])]
    # max_tide = curve_nel_vd.dissolve(by='voronoi_id', aggfunc='max')
    # min_tide = curve_nel_vd.dissolve(by='voronoi_id', aggfunc='min')
    # avg_tide = curve_nel_vd.dissolve(by='voronoi_id', aggfunc='mean')
    # median_tide = curve_nel_vd.dissolve(by='voronoi_id', aggfunc='median')
    curve_nel_polygon = curve_di_livello_4326[curve_di_livello_4326['V4W_ID']==polygon_id]
    if curve_nel_polygon.empty:
        print(f"Nessuna acqua alta in arco {polygon_id}")
        continue

    curve_nel_vd = gpd.overlay(curve_nel_polygon, vd, how='intersection')

    if curve_nel_vd.empty:
        print("Nessuna curva nei vd")
        continue

    min_tide = curve_nel_vd.groupby('voronoi_id')['LIVELLO_PS'].min().reindex(vd.index)
    max_tide = curve_nel_vd.groupby('voronoi_id')['LIVELLO_PS'].max().reindex(vd.index)
    avg_tide = curve_nel_vd.groupby('voronoi_id')['LIVELLO_PS'].mean().reindex(vd.index)
    median_tide = curve_nel_vd.groupby('voronoi_id')['LIVELLO_PS'].median().reindex(vd.index)
    #
    # edge_in_polygon['max_tide'] = max_tide #max(curve_nel_vd[curve_nel_vd['voronoi_id']==id])
    # edge_in_polygon['min_tide'] = min_tide #min(curve_nel_vd['LIVELLO_PS'])
    # edge_in_polygon['avg_tide'] = avg_tide
    # edge_in_polygon['median_tide'] = median_tide
    #    print("archi {}, min_tide {}".format(archi[archi['CVE_SCOD_V']==polygon_id], min_tide))
    archi.loc[archi['V4W_ID']==polygon_id,'max_tide'] = list(max_tide)
    archi.loc[archi['V4W_ID']==polygon_id,'min_tide'] = list(min_tide)
    archi.loc[archi['V4W_ID']==polygon_id,'avg_tide'] = list(avg_tide)
    archi.loc[archi['V4W_ID']==polygon_id,'med_tide'] = list(median_tide)
    print(f"Aggiunta acqua alta in arco {polygon_id}")

        # for alt in list_of_altitudes:
        #     curve_flooded = curve_di_livello[curve_di_livello['altitudine']<=alt]
            #for curve in curve_flooded
        #     polygon_flooded = curve_flooded.convex_hull

        # capisci i valori minimo, massimo e medio (usando il metodo di luca)

    # aggiungili al relativo arco del grafo (sappiamo qual è?)
    #archi_grafo_con_lo_stesso_id = [edge for edge in G_un.edges if edge['street_id'] == polygon_id]
    #archo_che_ci_serve = [edge for edge in archi_grafo_con_lo_stesso_id if geom_edges ]
    #arco_che_ci_serve = G_un[geom_edges.boundaries[0]][geom_edges.boundaries[1]]


    # edges.reset_index(drop=True)
    # edges_shapely = edges.unary_union #geom_edges = edges['geometry']
    # print(edges_shapely)
    # edges_areas = voronoi_diagram(edges_shapely, geom_polygon, tolerance=0.0, edges=False)
    # geom_polygon
    # edges_shapely
    # edges_areas
    # #print("edges {} correspond to {}".format(edges, edges_areas))
    # geoplot.polyplot(world, figsize=(8, 4))
    # #note that it is NOT supported to GeoDataFrame directly
    # gs = gpd.GeoSeries([edges_areas]).explode()
    # #convert to GeoDataFrame
    # #note that if gdf was shapely.geometry.MultiPolygon, it has no attribute 'crs'
    # gdf_vd_primary = gpd.geodataframe.GeoDataFrame(geometry=gs, crs=4326)
    # gpd.plot(gdf_vd_primary)
    # plt.plot(edges_areas)
    # plt.plot(geom_polygon)
	# #reset index
    # gdf_vd_primary.reset_index(drop=True)	#append(gdf)
    # #spatial join by intersecting and dissolve by `index_right`
    # gdf_temp = ( gpd.sjoin(gdf_vd_primary, gdf, how='inner', op='intersects')
	# 	.dissolve(by='index_right').reset_index(drop=True) )
    # gdf_vd = gpd.clip(gdf_temp, mask)
    # gdf_vd = dropHoles(gdf_vd)
#edge_dataframe.to_file(f'edges_df.geojson', driver= "GeoJSON")
# curve_nel_vd.groupby('voronoi_id')['LIVELLO_PS'].min().reindex(vd.index)
#
# edge_dataframe
# max_tide
# min_tide
# archi.loc[archi['CVE_SCOD_V']==44340, 'min_tide'] = list(min_tide)
# a = np.nan
# archi

#
# archi[archi['street_id']==polygon_id]['max_tide'] = max_tide
# vd

print('errors: ',err)
print('nan tides: ', len(archi[archi["max_tide"].isna()]))
print('num of edges: ', len(archi))
#%% Save output
# get original schema of the data (i.e. integer, string, float with respective width)
import fiona
with fiona.open(archi_path) as f:
    input_schema = f.schema
# add the new fields as integer
input_schema['properties']['max_tide'] = 'int:10'
input_schema['properties']['min_tide'] = 'int:10'
input_schema['properties']['avg_tide'] = 'int:10'
input_schema['properties']['med_tide'] = 'int:10'

folder_output = "/Users/ale/Downloads/v11/acquaalta"
name_output = "dequa_ve_terra_v11.shp"
if not os.path.exists(folder_output):
    os.mkdir(folder_output)
archi.to_file(os.path.join(folder_output, name_output), schema=input_schema)

#%%
from shapely.geometry import MultiPoint, MultiLineString
from shapely.ops import voronoi_diagram

from matplotlib import pyplot
from descartes.patch import PolygonPatch
from figures import SIZE, BLUE, GRAY, set_limits

points = MultiPoint([(0, 0), (1, 1), (0, 2), (2, 2), (3, 1), (1, 0)])
lines = MultiLineString([[(0,0), (1,1)], [(1.1,1.1), (2,2)]])
polygons = [Polygon([(0,0),(1,1),(0.9,0.9),(0.1,0.1)]),Polygon([(2,2),(3,3),(2.9,2.9),(2.1,2.1)])]
regions = voronoi_diagram(points)
regions_lines = voronoi_diagram(lines)
regions_polygons = voronoi_diagram(polygons)

fig = pyplot.figure(1, dpi=90)
fig.set_frameon(True)
ax = fig.add_subplot(111)

for region in regions:
    patch = PolygonPatch(region, facecolor='blue', edgecolor='blue', alpha=0.5, zorder=2)
    ax.add_patch(patch)

for point in points:
    pyplot.plot(point.x, point.y, 'o', color='black')

set_limits(ax, -1, 4, -1, 3)

pyplot.show()
#%%
def bufferDissolve(gdf, distance, join_style=3):
	'''Create buffer and dissolve thoese intersects.

	Parameters:
		gdf:
			Type: geopandas.GeoDataFrame
		distance: radius of the buffer
			Type: float
	Returns:
		gdf_bf: buffered and dissolved GeoDataFrame
			Type: geopandas.GeoDataFrame
	'''
	#create buffer and dissolve by invoking `unary_union`
	smp = gdf.buffer(distance, join_style).unary_union
	#convert to GeoSeries and explode to single polygons
	gs = gpd.GeoSeries([smp]).explode()
	#convert to GeoDataFrame
	gdf_bf = gpd.GeoDataFrame(geometry=gs, crs=gdf.crs).reset_index(drop=True)
	return gdf_bf

def voronoiDiagram4plg(gdf, mask):
	'''Create Voronoi diagram / Thiessen polygons based on polygons.

	Parameters:
		gdf: polygons to be used to create Voronoi diagram
			Type: geopandas.GeoDataFrame
		mask: polygon vector used to clip the created Voronoi diagram
			Type: GeoDataFrame, GeoSeries, (Multi)Polygon
	Returns:
		gdf_vd: Thiessen polygons
			Type: geopandas.geodataframe.GeoDataFrame
	'''
	gdf.reset_index(drop=True)
	#convert to shapely.geometry.MultiPolygon
	smp = gdf.unary_union
	#create primary voronoi diagram by invoking shapely.ops.voronoi_diagram (new in Shapely 1.8.dev0)
	smp_vd = svd(smp)
	#convert to GeoSeries and explode to single polygons
	#note that it is NOT supported to GeoDataFrame directly
	gs = gpd.GeoSeries([smp_vd]).explode()
	#convert to GeoDataFrame
	#note that if gdf was shapely.geometry.MultiPolygon, it has no attribute 'crs'
	gdf_vd_primary = gpd.geodataframe.GeoDataFrame(geometry=gs, crs=4326)

	#reset index
	gdf_vd_primary.reset_index(drop=True)	#append(gdf)
	#spatial join by intersecting and dissolve by `index_right`
	gdf_temp = ( gpd.sjoin(gdf_vd_primary, gdf, how='inner', op='intersects')
		.dissolve(by='index_right').reset_index(drop=True) )
	gdf_vd = gpd.clip(gdf_temp, mask)
	gdf_vd = dropHoles(gdf_vd)
	return gdf_vd

def dropHoles(gdf):
	'''Remove / drop / fill the holes / empties for iterms in GeoDataFrame.

	Parameters:
		gdf:
			Type: geopandas.GeoDataFrame
	Returns:
		gdf_nohole: GeoDataFrame without holes
			Type: geopandas.GeoDataFrame
	'''
	gdf_nohole = gpd.GeoDataFrame()
	for g in gdf['geometry']:
		geo = gpd.GeoDataFrame(geometry=gpd.GeoSeries(dropHolesBase(g)))
		gdf_nohole=gdf_nohole.append(geo,ignore_index=True)
	gdf_nohole.rename(columns={gdf_nohole.columns[0]:'geometry'}, inplace=True)
	gdf_nohole.crs = gdf.crs
	return gdf_nohole

def dropHolesBase(plg):
	'''Basic function to remove / drop / fill the holes.

	Parameters:
		plg: plg who has holes / empties
			Type: shapely.geometry.MultiPolygon or shapely.geometry.Polygon
	Returns:
		a shapely.geometry.MultiPolygon or shapely.geometry.Polygon object
	'''
	if isinstance(plg, MultiPolygon):
		return MultiPolygon(Polygon(p.exterior) for p in plg)
	elif isinstance(plg, Polygon):
		return Polygon(plg.exterior)
#%%
folder = "/Users/Palma/Documents/Githubs/v4w_website/app/static/files"
path_graph = os.path.join(folder, 'dequa_ve_terra_v8_dequa_ve_terra_0509_pickle_4326VE')
with open(path_graph, 'rb') as file:
    G_un = pickle.load(file)
G_un

# ciclo for su ogni arco
# PSEUDOCODICE:
# for each edge:
#    prendiamo la linea dell'arco
#    costruiamo una griglia di linee perpendicolari all'arco (in modo da avere la geometria)
#    per ogni linea perpendicolare:
#       fetchiamo massimo e minimo
#       intersezione tra le curve di livello e la linea perpendicolare
#    una volta finite le linee:
#       scegliamo massimo e minimo per arco e lo salviamo come attributo dell'arco
#       calcoliamo una media/mediana e la salviamo?
#    (opzionale):
#    guardiamo il nome e salviamo il nome della strada come attributo dell'arco

# parametri:
distance_sampling = 10e-7 # metro
from pprint import pprint
# ciclo for degli archi
for edge_coords in G_un.edges():
    # linea
    edge = G_un[edge_coords[0]][edge_coords[1]]
    geometry_edge = wkt.loads(edge['Wkt']).coords
    street_id = edge['street_id']
    if len(geometry_edge) < 2:
        raise Exception('The Edge is a point (???)')
    for idx_segment in range(len(geometry_edge)-1):
        segment = [geometry_edge[idx_segment], geometry_edge[idx_segment+1]]
        print(segment)
        # sampling della linea
        start_point = segment[0]
        end_point = segment[-1]
        length_segment = edge['length'] # in metri
        distance_points = np.sqrt(np.sum(np.power(np.subtract(end_point, start_point), 2)))
        print("dist: ", distance_points)
        num_steps = np.floor(distance_points/distance_sampling).astype(int)
        print("steps: ", num_steps)
        direction_vector = (np.subtract(end_point, start_point)) / num_steps
        rot_anti = np.array([[0, -1], [1, 0]])
        direction_vector_perp = np.dot(rot_anti, direction_vector) * 10e-5
        print("direction ", direction_vector)
        for n in range(num_steps):
            cur_sampling_point = start_point + n * direction_vector
            linestring_direction_perp = shapely.geometry.LineString([cur_sampling_point-direction_vector_perp, cur_sampling_point+direction_vector_perp])
            for j in range(len(geom_curves)):
                print(j)
                curve = geom_curves[j]
                intersection_ = curve.intersection(linestring_direction_perp)
                if (intersection_):
                    print("intersection between {} and {}".format(curve, linestring_direction_perp))
                    pprint(intersection_)

                print("finished")
            break
        break
    break
break
            #perp_line =

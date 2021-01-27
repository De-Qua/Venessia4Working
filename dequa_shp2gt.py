import sys
import geopandas as gpd

from graph_tool import Graph
from graph_tool.util import find_vertex

def progressbar(current_value,total_value,step=5,text='',progressSymbol='=',remainingSymbol=' ',currentSymbol=''):
    assert (100%step) == 0
    percentage = current_value / total_value * 100
    progress = int(percentage/step)
    remain = int(100/step-progress)
    if len(currentSymbol)>0:
        idx = current_value % len(currentSymbol)
        current = currentSymbol[idx]
    else:
        current = ''

    if percentage < 100:
        print("[{progress}{current}{remain}] {perc:5.1f}% {text}".format(progress=progressSymbol*progress,current=current,remain=remainingSymbol*(remain-len(current)),perc=percentage,text=text),
                                                    end="\r",flush=True)
    else:
        print("[{progress}{remain}] {perc:5.1f}% {text}".format(progress="="*progress,remain=" "*remain,perc=percentage,text=text),
                                                        end="\n",flush=True)


def retrieve_attribute_type(attribute):
    dequa_types = {
        'length': 'float',
        'ponte': 'int',
        'accessible': 'int',
        'street_id': 'float',
        'vel_max': 'float',
        'max_tide': 'float',
        'min_tide': 'float',
        'avg_tide': 'float',
        'med_tide': 'float',
        'pas_cm_zps': 'float',
        'pas_height': 'float',
        'geometry': 'object'
    }
    if attribute in dequa_types.keys():
        return dequa_types[attribute]
    else:
        return "No type detected"

def get_vertices_from_geometry(g, geometry):
    coord_source = geometry.coords[0]
    coord_target = geometry.coords[-1]
    latlon = g.vertex_properties['latlon']
    source = find_vertex(g, latlon, coord_source)
    if not source:
        source = g.add_vertex()
        g.vp.latlon[source] = coord_source
    else:
        source = source[0]
    target = find_vertex(g, latlon, coord_target)
    if not target:
        target = g.add_vertex()
        g.vp.latlon[target] = coord_target
    else:
        target = target[0]

    return source, target


def add_properties_to_edge(g, edge, properties):
    for property in properties.keys():
        g.ep[property][edge] = properties[property]
    return

def shp2gt(shp_path):
    print("Reading the file...")
    df = gpd.read_file(shp_path)

    print("The file has {} edges.".format(len(df)))
    print("Each edge has these attributes: {}".format([col for col in df.columns]))

    print("Creating the graph...")
    g = Graph(directed=False)

    # Add attributes as edge properties
    for col in df.columns:
        eprop = g.new_edge_property(retrieve_attribute_type(col))
        g.edge_properties[col] = eprop

    # Add the coordinates as vertex property
    vprop = g.new_vertex_property("vector<float>")
    g.vertex_properties['latlon'] = vprop

    print("Adding vertices and edges...")
    # Start extracting the info iterating by all the rows
    for index, row in df.iterrows():
        source, target = get_vertices_from_geometry(g, row['geometry'])
        edge = g.add_edge(source, target)
        # add the properties to the edge
        for property in row.keys():
            g.ep[property][edge] = row[property]
        progressbar(index+1, len(df))

    print("GRAPH PROPERTIES")
    print (g.list_properties())
    print("================")

    print("GRAPH ENTITY COUNT")
    print ("Vertices: {}".format(str(g.num_vertices())))
    print ("Edges: {}".format(str(g.num_edges())))
    print("================")

    return g


if __name__ == "__main__":

    print("\n******************************************")
    print(" ### SHP2GT ###")
    print("Let's convert a file shp to a graph in the graph-tool format!")
    print("******************************************\n")

    out_path = []
    if len(sys.argv) > 2:
        print("great, path is given as {}".format(sys.argv[1]))
        print("Also the output path is given as {}".format(sys.argv[2]))
        shp_path = sys.argv[1]
        out_path = sys.argv[2]
    elif len(sys.argv) > 1:
        print("great, path is given as {}".format(sys.argv[1]))
        print("We will use the same path as output (.gt)")
        #shp_path = os.path.join(sys.argv[1], shp_relative_path)
        shp_path = sys.argv[1]
    else:
        print("You must give a shp file in order to convert it to have graph!")

    if not out_path:
        pth, ext = os.path.splitext(shp_path)
        out_path = os.path.join(pth,'.gt')

    graph = shp2gt(shp_path)
    graph.save(out_path)

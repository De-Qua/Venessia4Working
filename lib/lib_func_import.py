import networkx as nt
import pickle
from geopy.distance import distance

def lines_length(series):
    """Calculate lengths of geopandas series of lines in meters
    Args:
        series: a geopandas series of LineString objects with WGS 84 coordinates

    Returns:
        Series of lengths of lines in meters
    """
    return series.apply(line_length)

def line_length(line):
    """Calculate length of a line in meters, given in geographic coordinates.
    Args:
        line: a shapely LineString object with WGS 84 coordinates

    Returns:
        Length of line in meters

    Source:
        https://gis.stackexchange.com/a/115285
    """
    # Swap shapely (lonlat) to geopy (latlon) points
    latlon = lambda lonlat: (lonlat[1], lonlat[0])
    total_length = sum(distance(latlon(a), latlon(b)).meters
                       for (a, b) in pairs(line.coords))
    return total_length


def pairs(lst):
    """Iterate over a list in overlapping pairs without wrap-around.

    Args:
        lst: an iterable/list

    Returns:
        Yields a pair of consecutive elements (lst[k], lst[k+1]) of lst. Last
        call yields the last two elements.

    Example:
        lst = [4, 7, 11, 2]
        pairs(lst) yields (4, 7), (7, 11), (11, 2)

    Source:
        https://stackoverflow.com/questions/1257413/1257446#1257446
    """
    i = iter(lst)
    prev = next(i)
    for item in i:
        yield prev, item
        prev = item

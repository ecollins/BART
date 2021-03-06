#! /usr/bin/env python
import googlemaps
import numpy as np
import pandas as pd

def ITEMS(dct):
    try:
        xrange
        return dct.iteritems()
    except NameError:
        return dct.items()
    
def gmapsClient(keyfile="../keys/GoogleMaps_GeocodingAPI_Key_Elliott"):

    try: keyfile.geocode #~ Check if it's already an argument:w
    except (NameError, AttributeError):
        with open(keyfile) as F: KEY = F.read()
        gmaps = googlemaps.Client(key=KEY)
    return gmaps
    
def print_dict(d,indent=0):
    """
    Pretty indented format for printing nested dictionaries like the ones
    returned by the gmaps api.
    """
    STRING = ""
    if type(d)==list:
        for item in d:
            STRING+= print_dict(item,indent=indent)
    elif type(d)!=dict: STRING += "\t"*(indent)+str(d)+"\n"
    else:
        for k,v in d.items():
            K = str(k)
            #~ Underlined key name
            STRING += "{}{}\n{}{}\n".format("\t"*indent,K,"\t"*indent,"-"*len(K))
            STRING += print_dict(v,indent=indent+1)

    return STRING

def e0(x):
        try: return x[0]
        except TypeError: x

def e1(x):
    try: return x[1]
    except TypeError: x

def location_names(d,location="location",join=True):
    """
    Pull location names from API Results
    """
    if pd.isnull(d): return d
    names = [i['long_name'] for i in d['address_components']]
    if join: names = "; ".join(names)
    return names

def latlon(d,location="location"):
    """
    Pull latitude and longitude out of a googlemaps client result
    """
    if pd.isnull(d): return d
    if location   == "location": location = [ d["geometry"][location] ]
    elif location in ("viewport","bounds"): location = [ d["geometry"][location][i] for i in ("northeast","southwest") ]
    else: raise KeyError("Location {} is not a Google Maps Attribute.".format(location))
        
    spot = [(loc["lat"],loc["lng"]) for loc in location]
    if location=="location": return spot[0]
    else: return spot

def geolocations(Locations,gmaps,verbose=20, names = False, return_errors=False):
    """
    For a location and a google maps client,
        return a dictionary {location: (latitude,longitude)}

    (if gmaps is a string, use it as the API key and make the client object.)
    """

    if type(gmaps)==str: gmaps = googlemaps.Client(key=gmaps)

    gmap_results,counter,errors = {},0, []
    geo_dict = {}
    for counter, location in enumerate(Locations):
        #~ Pull Client result object for each location string in list & put latlon in geodict
        try:
            gmap_results[location] = gmaps.geocode(location)
            geo_dict[location]=gmap_results[location][0]
        except:
            errors.append(location)
            print("Error with location: {}".format(location))
            geo_dict[location]=np.nan
            continue

        if verbose and (not counter%verbose): print("{}: {}".format(counter,location))
    
    result = {loc : latlon(geo_dict[loc]) for loc in Locations}

    if names: names = {loc : location_names(geo_dict[loc]) for loc in Locations}
    if return_errors and names: return result, names, errors
    elif return_errors: return result, errors
    elif names: return result, names
    else: return result

def test(client):
    """
    Make sure the relevant functions work
    """
    result = geolocations(["San Francisco, CA","1354 28th St South, Arlington, VA"], gmaps=client)
    return result

if __name__ == '__main__':

    gmaps   = gmapsClient()
    results = test(gmaps)

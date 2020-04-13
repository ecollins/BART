#~ Imports & globals
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import geocoding as geo
plot_jsons = {}

def toInt(x):
    try: return int(x)
    except: return x

def graph_javascript(graphdiv,graphjson,positiondiv):
    
    script_template = """<style>
        var graphDiv = document.getElementById('{positiondiv}');
        var newGraph  = document.createElement('{graphdiv}');
        graphDiv.parentNode.insertBefore(newGraph, graphDiv);

            Plotly.d3.json("{graphjson}", function(plotly_data) {
            var config = {responsive: true}
            Plotly.newPlot('{graphid}', plotly_data.data, plotly_data.layout, config ); })
        </style>
        """
    txt = script_template.format(graphdiv=graphdiv,graphjson=graphjson,positiondiv=positiondiv)
    return txt

def expressMap():
    """
    from https://plotly.com/python/scattermapbox/
    """
    df = px.data.carshare()
    fig = px.scatter_mapbox(df, lat="centroid_lat", lon="centroid_lon",     color="peak_hour", size="car_hours",
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
    return fig


def stationMap():
    """
    from https://plotly.com/python/scattermapbox/
    """
    df = station_data
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="rides2020", color="parking",
                    color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10)
    return fig


def ride_data(File,columns=['date','hour','enter','exit','rides'],**kwargs):
    """
    
    """
    B = pd.read_csv(File,header=None,names=columns,**kwargs)
    B['date'] += B['hour'].apply(lambda h: " {:02d}:00:00".format(h))
    B['date'] = pd.to_datetime(B['date'])
    B = B.drop('hour',axis=1).set_index(['date','enter','exit'])
    B = B.unstack('exit').fillna(0)['rides']
    
    return B

def station_locations(station_df,client):
    """
    Get station latlons from Google API
    """
    addresses = station_df['Station']+" BART Station, " + station_df['Location']+", CA"
    codes = dict(zip(addresses, station_df['enter']))

    latlons = geo.geolocations(addresses, client)
    result = {}
    for address, loc in geo.ITEMS(latlons):
        try: loc[0][0] #~ make sure it's the normal [(lat,lon)] format
        except: loc = [loc] #~ Otherwise it's np.nan
        result[codes[address]] = loc[0]
    return result

def station_data(File,get_latlons=False):
    """
    
    """
    stations = pd.read_csv(FILE)

    #~ Get locations
    if get_latlons or ('lat' not in stations):
        ask = input("Getting station latlons. Exit script to not")
        locations = station_locations(stations,gmaps)
        stations['geo']= stations['enter'].map(locations)
        stations['lat']= [l[0] for l in stations.geo]
        stations['lon']= [l[1] for l in stations.geo]
        stations = stations.set_index("enter")
        stations.to_csv("../data/stations.csv", index=True)
    else: stations = stations.set_index("enter")

    return stations


if __name__ == '__main__':
    #~ Various clients
    with open("../../../.mapbox_token") as token: px.set_mapbox_access_token(token.read())
    gmaps = geo.gmapsClient()
    
    #~ Read & Prep Datasets
    B = ride_data("../data/date-hour-soo-dest-2020.csv")
    stations = station_data("../data/stations.csv")

    codes = stations['enter'].to_list()
    codes.remove("MLPT")

    fig = stationMap()
    fig.show()

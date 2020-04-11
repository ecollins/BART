#~ Imports & globals
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

if __name__ == '__main__':
    px.set_mapbox_access_token(open("../../../.mapbox_token").read())
    fig = expressMap()
    fig.show()

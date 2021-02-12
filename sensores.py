import numpy as np                   # for multi-dimensional containers 
import pandas as pd                  # for DataFrames
import plotly.graph_objects as go    # for data visualisation
import plotly.express as px

import psycopg2
from psycopg2 import Error
from psycopg2 import connect, sql 
#import pandas as pd
import pandas.io.sql as sqlio
from timeit import default_timer as timer
from datetime import timedelta
#from psycopg2 import ProgrammingError, errorcodes, errors
import geopandas as gpd

access_token = 'pk.eyJ1Ijoic2NpZW50aWZpY2RldGVjdGl2ZXNhZ2VuY3kiLCJhIjoiY2p6aHFmaHlpMHlmOTNucWtrd2FyMzlndCJ9.bBgagYmGca64Y5VZYe9UNA'
px.set_mapbox_access_token(access_token)

def make_conn ():
    connection = psycopg2.connect(user="postgres",
                        password="G301nt43",
                        host="192.168.0.117",
                        port="5432",
                        database="pulso_digital",
                        )
    return connection

def sensor_table(sensor_list): 
    ##Hace un append por cada tabla de sensor con sus valores## 
    connection = make_conn()
    dfs = {}
    for i in range(len(sensor_list)):
        connection = make_conn()
        sensor_data = {
            "sensor_id" : sensor_list[i]
            } 
        sql = """WITH sens AS (SELECT * FROM tmp.sensores WHERE sensores.id = %(sensor_id)s),
        vels AS (SELECT ts, valores[%(sensor_id)s] FROM tmp.velocidades)
        SELECT sens.*, vels.* FROM sens JOIN vels ON sens.id = %(sensor_id)s ORDER BY ts ASC;""" % sensor_data
        print(sql)
        #dfs[i] = gpd.read_postgis(sql, connection)
    return pd.concat(dfs)


sensors = sensor_table(sensor_list)    
sensors = df.filter(["id","ts", "ubicacion", "latitude", "longitude", "valores"]) 
sensors['date'] = sensors['ts'].dt.strftime('%Y-%m-%d')
date_mask = sensors['date'] == sensors['date'].max()

### mapa estatico con los sensores

fig = px.scatter_mapbox(
    sensors[date_mask], lat="latitude", lon="longitude",
    size="valores", size_max=50,
    color="valores", color_continuous_scale=px.colors.sequential.Pinkyl,
    hover_name="ubicacion",           
    mapbox_style='dark', zoom=1
)
fig.layout.coloraxis.showscale = False
fig.show()

## Animación con slider
fig = px.scatter_mapbox(
    sensors, lat="latitude", lon="longitude",
    size="valores", size_max=30,
    color="valores", color_continuous_scale=px.colors.sequential.Pinkyl,
    hover_name="ubicacion",           
    mapbox_style='dark', zoom=1,
    animation_frame="date", animation_group="ubicacion"
)
    
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
fig.layout.coloraxis.showscale = False
fig.layout.sliders[0].pad.t = 10
fig.layout.updatemenus[0].pad.t= 10
fig.show()
    
    
 

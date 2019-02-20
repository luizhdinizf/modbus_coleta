#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 18:34:18 2018

@author: luiz
"""


import pandas as pd
import numpy as np
import plotly.graph_objs as go



#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
#plotly.tools.set_credentials_file(username='luizhdinizf', api_key='AMwGYVDfoDhbmJT1TFp7')
#plotly.tools.set_config_file(world_readable=True,
#                             sharing='public')

filename = '/home/luiz/Fiat/Energy/log.log'      # size 90 GB
def loadfile(filename):
    chunksize = 10**5   
    df_big= pd.read_json(filename, lines=True,chunksize=chunksize)
    df = []
    for chunk in df_big:
        df.append(chunk)
    df = pd.concat(df)
    formata = '%Y-%m-%d %H:%M:%S'
    df['time'] = pd.to_datetime(df['time'],format=formata)
#    df.index=pd.DatetimeIndex(df['time'])

    df.index=df['time']
    df['time'] = str(df['time'])
#    df.drop('time')
    #print(str(getsizeof(df)/1000000)+' Mb')
    return(df)
def resample_and_plot(df,address,params,interval,mean_interval):    
    title = params['title'] 
    a = df.loc[df['address'] == address]       
    a=a.resample(interval).mean()    
#    py.plot([{
#        'x': pd.to_datetime(a.index).tolist(),
#        'y': a['decoded_instant'],
#        'name': 'instant'
#        }] ,kind='area', filename='simple-line_'+str(address), fill='tonexty')   
    trace1 = go.Scatter(
    x=pd.to_datetime(a.index).tolist(),
    y=a['decoded_instant'],
    fill='tonexty',
    name='Fluxo de Ar NM³/h'
    )
    thres = 1
    cut = a[a.decoded_instant>thres]['decoded_instant'].mean()
    std = a[a.decoded_instant>thres]['decoded_instant'].std()
    std_high = std/5
    std_low = -std/5
    x_cutted=pd.to_datetime(a[a.decoded_instant>cut].index).tolist()
    
    trace2 = go.Scatter(
    x=x_cutted,
    y=a[a.decoded_instant>cut]['decoded_instant'].rolling(mean_interval).mean()+std_high,
    name='Banda Alta'
    )
    
    trace3 = go.Scatter(
    x=x_cutted,
    y=a[a.decoded_instant>cut]['decoded_instant'].rolling(mean_interval).mean()+std_low,
    name='Banda Baixa'
    )
    
    trace4 = go.Scatter(
    x=x_cutted,
    y=a[a.decoded_instant>cut]['decoded_instant'].rolling('1800S').mean(),
    name='Média'
    )    
    
    
    
    data = [trace1,trace2,trace3,trace4]
    
    layout = dict(title = title,
              yaxis = dict(zeroline = False),
              xaxis = dict(zeroline = False)
             )
    fig = dict(data=data, layout=layout)

    return fig

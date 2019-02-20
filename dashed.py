import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
import plotly_big_data

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
filename = '/home/luiz/Fiat/Energy/log.log' 

df = plotly_big_data.loadfile(filename)
lista_trechos=[1,2,4,6,8,10]
def transform_value(value):
    return 10 ** value
print("loaded")
app.layout = html.Div([
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed=dt(1995, 8, 5),
        max_date_allowed=dt(2017, 9, 19),
        initial_visible_month=dt(2017, 8, 5),
        end_date=dt(2017, 8, 25)
    ),
    html.Div([
        dcc.Dropdown(
                id='trechos',
                options=[{'label': "Trecho: "+str(lista_trechos[i-1]), 'value': i} for i in range(1,7)],
                value=1
            ),        
            
            ]),
        
    dcc.Graph(id='graph-with-slider'),
    
    
    dcc.Slider(
        id='intervalos',
        marks={i: '{}'.format(10 ** i) for i in range(6)},
        max=5,
        value=2,
        step=0.1,
        updatemode='drag'
    ),
    html.Div(id='updatemode-output-container', style={'margin-top': 20})
])


@app.callback(
    dash.dependencies.Output('graph-with-slider', 'figure'),
    [dash.dependencies.Input('trechos', 'value'),   
     dash.dependencies.Input('intervalos', 'value')
                                                     ]    
    )
def update_figure(trecho,intervalo):
    intervalo=transform_value(intervalo)
    intervalo = str(int(intervalo))+'S'
    params =[]
    params['title'] = 'Trecho:'+str(lista_trechos[trecho-1])
    fig=plotly_big_data.resample_and_plot(df,trecho,params,intervalo,'3600S')
    return fig

@app.callback(Output('updatemode-output-container', 'children'),
              [Input('intervalos', 'value')])
def display_value(value):
    intervalo=transform_value(value)
    intervalo = str(int(intervalo))+'S'
    return 'Média em: ' + intervalo
    


if __name__ == '__main__':
    app.run_server(debug=True)
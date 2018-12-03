
# coding: utf-8

# In[ ]:


import dash
from dash.dependencies import Input, Output 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

euro_data = pd.read_csv("Eurostat_file.csv")
available_indicators = euro_data['NA_ITEM'].unique()
available_countries = euro_data['GEO'].unique()

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
euro_data1 = euro_data[euro_data['UNIT'] == 'Current prices, million euro']

app.layout = html.Div([
    html.H2('Final Assignment Anthony Van Praet',style={'textAlign': 'left', 'color': 'blue'}),
    html.H4('Graph 1',style={'textAlign': 'center'}),
    html.Div([ #chart number 1
        html.Div([
            dcc.Dropdown( #1 dropdown indicators with default value
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown( #2 dropdown indicators with default value
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries'
            )
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='grph1'),
    html.Div(dcc.Slider( #3 slider dependent on timing
        id='year--slider',
        min=euro_data['TIME'].min(),
        max=euro_data['TIME'].max(),
        value=euro_data['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in euro_data['TIME'].unique()},
    
    ), style={'marginRight': 50, 'marginLeft': 110},),

    html.H4('Graph 2',style={'textAlign': 'center'}),
    html.Div([ #chart number 2
        html.Div([
            dcc.Dropdown( #1 van second chart, indicators
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),
       html.Div([
            dcc.Dropdown( #2 van second chart, countries
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= "Spain"
                
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
     dcc.Graph(id='grph2'),


])

@app.callback( #callback first chart
    dash.dependencies.Output('grph1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    euro_data_yearly = euro_data[euro_data['TIME'] == year_value]
    return {
        'data': [go.Scatter(
            x=euro_data_yearly[euro_data_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            y=euro_data_yearly[euro_data_yearly['NA_ITEM'] == yaxis_column_name]['Value'],
            text=euro_data_yearly[euro_data_yearly['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }

@app.callback( #callback second chart
    dash.dependencies.Output('grph2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name):
    euro_data_yearly = euro_data1[euro_data1['GEO'] == yaxis_column_name]
    return {
        'data': [go.Scatter(
            x=euro_data_yearly['TIME'].unique(),
            y=euro_data_yearly[euro_data_yearly['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()


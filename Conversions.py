# -*- coding: utf-8 -*-
"""
Created on Sun Aug 21 14:07:08 2022

@author: ahnjiw
"""

import pyproj

import dash
from dash import dcc, html
from dash.dependencies import Input, Output , State
import dash_bootstrap_components as dbc

# Colors
bmao = '#f7923a'
bmar = '#ee3b34'
bmab = '#004890'

# Initiate the app
external_stylesheets = [dbc.themes.SANDSTONE]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'PDM Coordinate Converter'

def convert(x, y, mode):
    mycrs = open(r"PDMG.prj", "r").read()
    
    if mode:
        inproj = 4326
        outproj = pyproj.crs.CRS(mycrs)
    else:
        outproj = 4326
        inproj = pyproj.crs.CRS(mycrs)
    
    #create transformation
    proj = pyproj.Transformer.from_crs(inproj, outproj, always_xy=True)
    
    # calculate new location
    x2,y2 = proj.transform(x, y)
    return x2, y2

colors = {
    'background': '#000000',
    'text': '#373D3F'
}

modes = ['WGS84 to Peak Downs Grid', 'Peak Downs Grid to WGS84']
mode = dbc.RadioItems(
                id="mode-state",
                options=[{"label": x, "value": x} for x in modes],
                value='WGS84 to Peak Downs Grid'
            )

inputstyle = {'width': '150px', 'display':'inline-block', 'margin-left':'10px','vertical-align':'middle', 'fontsize' : 14}

outputstyle = {'width': '200px', 'display':'inline-block', 'margin-left':'10px','vertical-align':'middle', 'fontsize' : 14}

# Server
app.layout = html.Div([
    html.H3(children=[html.Span("Convert WGS84 to ", style={'color': colors['text']}),
                      html.Span("Peak ", style={'color':bmao}),
                      html.Span("Downs ", style={'color':bmar}),
                      html.Span("Mine ", style={'color':bmab}),
                      html.Span("Grid", style={'color': colors['text']})],
            style={'textAlign': 'center','font-family':'Verdana','color': colors['text'],'padding-top': 20}),
    
    html.Hr(),
    
        html.Div([html.Label(["Conversion Mode ",
                          mode])],
         style={'vertical-align':'middle','margin-top':'10px','font-size':16,'font-family':'Verdana','textAlign':'center','color':colors['text']}),
        
    html.Div([html.Label(["Input Easting (Longitude) and Northing (Lattitude) ",
                          dcc.Input(id='X1-state', type='number', inputMode = 'numeric', style=inputstyle),
                          dcc.Input(id='Y1-state', type='number', inputMode = 'numeric', style=inputstyle)])],
         style={'vertical-align':'middle','margin-top':'10px','font-size':16,'font-family':'Verdana','textAlign':'center','color':colors['text']}),

    html.Div([html.Button('Convert', id='update_button-state', n_clicks=0)],
             style={'vertical-align':'middle','margin-top':'10px','font-size':10,'font-family':'Verdana','textAlign':'center','color':colors['text']}),
    
    html.Hr(),
    
    html.Div([html.Label(["Converted Easting (Longitude) and Northing (Lattitude) ",
                      html.Div(id='X2-state',  style=outputstyle),
                      html.Div(id='Y2-state', style=outputstyle)])],
     style={'vertical-align':'middle','margin-top':'10px','font-size':16,'font-family':'Verdana','textAlign':'center','color':colors['text']}),
    
    html.Hr(),
    
    html.Div(dcc.Markdown('''
                          
    _Created by : Jiwoo Ahn_
    
    '''), style = {'font-size':10,'font-family':'Verdana','textAlign':'center','color':colors['text']}),
])

@app.callback(
    Output('X2-state', 'children'),
    Output('Y2-state', 'children'),
    Input('update_button-state', 'n_clicks'),
    State('X1-state', 'value'),
    State('Y1-state', 'value'),
    State('mode-state', 'value'),
)

#   joint1_dip, joint1_dd, joint2_dip, joint2_dd, joint3_dip, joint3_dd, fric_ang
def update_output_div(n_clicks, X1, Y1, mode):
    if n_clicks > 0 and X1 and Y1:
        print(n_clicks)
        if mode == 'WGS84 to Peak Downs Grid':
            modeBool = True
        else:
            modeBool = False
        
        X2, Y2 = convert(X1, Y1, modeBool)
        
        return str(X2), str(Y2)

if __name__ == "__main__":
    app.run_server()
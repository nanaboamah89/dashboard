import dash
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np

import plotly.express as px


BA=pd.read_excel("exported data from Ahafo Region.xlsx")
AS=pd.read_excel("exported data from Ashanti Region.xlsx")
ES=pd.read_excel("Exported data from Eastern Region.xlsx")
GR=pd.read_excel("exported data from Greater Accra Region.xlsx")
ba = BA.iloc[:,0:12]
gr = GR.iloc[:,0:12]
ash = AS.iloc[:,0:12]
es = ES.iloc[:,0:12]
df = ba.append(ba).append(gr).append(ash).append(es)

nregions =df.Regions.unique()

#Choose a theme and define the layout
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


# the style arguments for the sidebar.
SIDEBAR_STYLE = {
     'position': 'fixed',
     'top': 0,
     'left': 0,
     'bottom': 0,
     'width': '20%',
     'padding': '20px 10px',
     'background-color': '#ffd697',
     
 }

# the style arguments for the main content page.
CONTENT_STYLE = {
     'margin-left': '25%',
     'margin-right': '5%',
     'padding': '20px 10p'
 }

TEXT_STYLE = {
     'textAlign': 'center',
     'color': '#191970'
 }

CARD_TEXT_STYLE = {
     'textAlign': 'center',
     'color': '#0074D9'
 }
#######Drop downs
controls = dbc.FormGroup(
     [
         html.Br(),
         html.P('Region', style={
             'textAlign': 'center'
         }),
         dcc.Dropdown(
             id='region-dropdown',
             
             options=[{"label": nr, "value": nr} for nr in np.sort(nregions)]
             ,
# default value
             multi=False
        
         ),
         html.Br(),
         html.P('District', style={
             'textAlign': 'center'
         }),
         dcc.Dropdown(
             id='district-dropdown',
             options=[]
             ,
# default value
             multi=False
         ),
         html.Br(),
         html.P('Indicators', style={
             'textAlign': 'center'
         }),
         dcc.Dropdown(
             id='indicators-dropdown',
             
             options=[
                 {"label": 'Age', "value": 'Age'},
                 {"label": 'Sex', "value": 'Sex'},
                 {"label": 'Education', "value": 'Education'}
                     ]
             ,
# default value
             multi=False
         ),
     ]
 )

sidebar = html.Div(
     [
         html.H2('Parameters', style=TEXT_STYLE),
         html.Hr(),
         controls
     ],
style=SIDEBAR_STYLE,
 )

# #Graph Items
content_third_row = dbc.Row(
     [
         html.Br(),
         html.P('What type of economic activity are you engaged in?', style={
             'textAlign': 'center'
         }),
         html.Br(),
  
        html.Div(
            children=dcc.Graph(
                id="type-chart"
            ),
            className="card",
            
        ),
     ]
 )

content_indicator_row = dbc.Row(
       [
          html.Br(),
         html.P('Are you engaged in any economic activity?', style={
             'textAlign': 'center'
         }),
           html.Br(),
           
        html.Div(
            children=dcc.Graph(
                id="eco-chart"
            ),
            className="card",
            
        ),
 
     ]
 )

content_secu_row = dbc.Row(
       [
          html.Br(),
         html.P('Would you describe the current security situation in the country as secured?', style={
             'textAlign': 'center'
         }),
           html.Br(),
        html.Div(
            children=dcc.Graph(
                id="secu-chart"
            ),
            className="card",
            
        ),

     ]
 )

content_con_row = dbc.Row(
       [
            html.Br(),
         html.P('Do you have confidence in the ability of security agencies to contain the security situation?',
                style={
             'textAlign': 'center'
         }),
    
        html.Div(
            children=dcc.Graph(
                id="con-chart"
            ),
            className="card",
            
        ),
      
     ]
 )

content_safe_row = dbc.Row(
       [
        html.Br(),
         html.P('Do you feel safe in the country?',
                style={
             'textAlign': 'center'
         }),
           html.Br(),
        html.Div(
            children=dcc.Graph(
                id="safe-chart"
            ),
            className="card",
            
        ),
     
     ]
 )


content = html.Div(
     [

         content_indicator_row,
         content_third_row,
         content_secu_row,
         content_con_row,
         content_safe_row
     ],
     style=CONTENT_STYLE
 )


app.layout = html.Div([sidebar, content])

@app.callback(
    Output("district-dropdown", "options"),
    [Input("region-dropdown", "value")],
)
def update_districts(region):
    district= (df[df['Regions'] == str(region)]['District']).unique()
    options = [{"label": nr, "value": nr} for nr in np.sort(district)]

    return options


@app.callback(
   [Output("eco-chart", "figure"),
    Output("type-chart", "figure"),
    Output("secu-chart", "figure"),
    Output("safe-chart", "figure"),
    Output("con-chart", "figure")],
    [Input("region-dropdown", "value"),
    Input("district-dropdown", "value"),
    Input("indicators-dropdown", "value")],
)
def submit_(region, district, indicators):   
    if district:
        if indicators == 'Age':
            
            x_bar = 'Age'
                
            c_bar = 'Are you engaged in any economic activity?'
            eco_result = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar]
            ).count()
            
            c_bar_econ = 'What type of economic activity are you engaged in?'
            eco_type = result = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_econ]
            ).count()
            
            c_bar_secu = 'Would you describe the current security situation in the country as secured?'
            eco_secu = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_secu]
            ).count()
            
            c_bar_safe = 'Do you feel safe in the country?'
            eco_safe = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_safe]
            ).count()
            
            c_bar_con = 'Do you have confidence in the ability of security agencies to contain the security situation?'
            eco_con = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_con]
            ).count()
            
            
        elif indicators == 'Sex':
            
            x_bar = 'Sex'
                
            c_bar = 'Are you engaged in any economic activity?'
            eco_result = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar]
            ).count()
            
            c_bar_econ = 'What type of economic activity are you engaged in?'
            eco_type = result = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_econ]
            ).count()
            
            c_bar_secu = 'Would you describe the current security situation in the country as secured?'
            eco_secu = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_secu]
            ).count()
            
            c_bar_safe = 'Do you feel safe in the country?'
            eco_safe = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_safe]
            ).count()
            
            c_bar_con = 'Do you have confidence in the ability of security agencies to contain the security situation?'
            eco_con = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_con]
            ).count()
            
            
            
        elif indicators == 'Education':
            
            x_bar = 'What is your level of education?'
                
            c_bar = 'Are you engaged in any economic activity?'
            eco_result = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar]
            ).count()
            
            c_bar_econ = 'What type of economic activity are you engaged in?'
            eco_type = result = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_econ]
            ).count()
            
            c_bar_secu = 'Would you describe the current security situation in the country as secured?'
            eco_secu = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_secu]
            ).count()
            
            c_bar_safe = 'Do you feel safe in the country?'
            eco_safe = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_safe]
            ).count()
            
            c_bar_con = 'Do you have confidence in the ability of security agencies to contain the security situation?'
            eco_con = df[df['District'] == str(district)].groupby(
                [x_bar, c_bar_con]
            ).count()
            
            lab = district
        
    elif region:
        
        if indicators == 'Age':
            
            x_bar = 'Age'
                
            c_bar = 'Are you engaged in any economic activity?'
            eco_result = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar]
            ).count()
            
            c_bar_econ = 'What type of economic activity are you engaged in?'
            eco_type = result = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_econ]
            ).count()
            
            c_bar_secu = 'Would you describe the current security situation in the country as secured?'
            eco_secu = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_secu]
            ).count()
            
            c_bar_safe = 'Do you feel safe in the country?'
            eco_safe = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_safe]
            ).count()
            
            c_bar_con = 'Do you have confidence in the ability of security agencies to contain the security situation?'
            eco_con = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_con]
            ).count()
            
            
        elif indicators == 'Sex':
            
            x_bar = 'Sex'
                
            c_bar = 'Are you engaged in any economic activity?'
            eco_result = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar]
            ).count()
            
            c_bar_econ = 'What type of economic activity are you engaged in?'
            eco_type = result = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_econ]
            ).count()
            
            c_bar_secu = 'Would you describe the current security situation in the country as secured?'
            eco_secu = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_secu]
            ).count()
            
            c_bar_safe = 'Do you feel safe in the country?'
            eco_safe = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_safe]
            ).count()
            
            c_bar_con = 'Do you have confidence in the ability of security agencies to contain the security situation?'
            eco_con = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_con]
            ).count()
            
            
            
        elif indicators == 'Education':
            
            x_bar = 'What is your level of education?'
                
            c_bar = 'Are you engaged in any economic activity?'
            eco_result = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar]
            ).count()
            
            c_bar_econ = 'What type of economic activity are you engaged in?'
            eco_type = result = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_econ]
            ).count()
            
            c_bar_secu = 'Would you describe the current security situation in the country as secured?'
            eco_secu = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_secu]
            ).count()
            
            c_bar_safe = 'Do you feel safe in the country?'
            eco_safe = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_safe]
            ).count()
            
            c_bar_con = 'Do you have confidence in the ability of security agencies to contain the security situation?'
            eco_con = df[df['Regions'] == str(region)].groupby(
                [x_bar, c_bar_con]
            ).count()
            
            
           
        lab = region
        
    else:
        pass
        
    
    eco_result = eco_result.reset_index()
    eco_result['count'] = eco_result['Regions']
    
    eco_type = eco_type.reset_index()
    eco_type['count'] = eco_type['Regions']
    
    eco_secu = eco_secu.reset_index()
    eco_secu['count'] = eco_secu['Regions']
    
    eco_safe = eco_safe.reset_index()
    eco_safe['count'] = eco_safe['Regions']
    
    eco_con = eco_con.reset_index()
    eco_con['count'] = eco_con['Regions']


    eco_chart_figure = px.bar(
        eco_result, x=x_bar, y="count", 
        color=c_bar)
    type_chart_figure = px.bar(
        eco_type, x=x_bar, y="count", 
        color=c_bar_econ)
    secu_chart_figure = px.bar(
        eco_secu, x=x_bar, y="count", 
        color=c_bar_secu)
    safe_chart_figure = px.bar(
        eco_safe, x=x_bar, y="count", 
        color=c_bar_safe)
    con_chart_figure = px.bar(
        eco_con, x=x_bar, y="count", 
        color=c_bar_con)
    
    return eco_chart_figure, type_chart_figure, secu_chart_figure, safe_chart_figure, con_chart_figure


if __name__ == '__main__':
    app.run_server(debug=True)

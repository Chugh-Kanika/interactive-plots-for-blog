import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df_flat = pd.read_csv('Dashboard_file preprocessed df.csv')
available_country = df_flat['Country Name'].unique()

#Below code defines the layout of the dashboard. It defines how the dashboard will appear as a web page.
#For this dashboard, there are two dropdowns to select two countries for comparison and two time series chart for the
#pre-defined parameter which get updated based on the country selected.

#Dash Core Component - Dropdown and Graph is being used where Time-series graph will update based on country selected
app.layout = html.Div(children=[
    html.H1(children='Climate Change Dashboard', style={
        'textAlign': 'center'
    }),

    html.Div(children='''
      Select Countries for comparative analysis''', style={
        'textAlign': 'center'
    })
    ,

    html.Div([
        html.Div([
            dcc.Dropdown(
                id='country1',
                options=[{'label': i, 'value': i} for i in available_country],
                value='China', clearable=False
            )], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='country2',
                options=[{'label': i, 'value': i} for i in available_country],
                value='United States', clearable=False
            )], style={'width': '49%', 'display': 'inline-block'})],
        style={'borderBottom': 'thin lightgrey solid',
               'backgroundColor': 'rgb(250, 250, 250)',
               'padding': '10px 5px'}),
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        ),
        html.Div([
            html.Div([
                dcc.Graph(id='x-time-series1')], style={'width': '49%', 'display': 'inline-block'}),

            html.Div([
                dcc.Graph(id='y-time-series1')], style={'width': '49%', 'display': 'inline-block'})],
            style={'borderBottom': 'thin lightgrey solid',
                   'backgroundColor': 'rgb(250, 250, 250)',
                   'padding': '10px 5px'}
        )

    ])
])


# Below code defines the callback in the dashboard, callbacks add the interactivity in dashboard,
# Input value is from the dropdown and output is the time series chart
@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'), dash.dependencies.Output('y-time-series', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
# Below code defines the function that will create a dataframe and a time series graph based on country selected in the dropdown.

def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name'] == 'CO2 emissions (kt)']
    maxv = CO2_df.nlargest(1, 'value')['value'].values.tolist()
    minv = CO2_df.nsmallest(1, 'value')['value'].values.tolist()

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name'] == 'CO2 emissions (kt)']

    maxv2 = CO2_df2.nlargest(1, 'value')['value'].values.tolist()
    minv2 = CO2_df2.nsmallest(1, 'value')['value'].values.tolist()

    maxva2 = max(maxv + maxv2)
    minva2 = min(minv + minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='CO2 emissions (kt)',
                      range_y=[minva2, maxva2])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='CO2 emissions (kt)',
                      range_y=[minva2, maxva2])
    return figure1, figure2

@app.callback(
    dash.dependencies.Output('x-time-series1', 'figure'), dash.dependencies.Output('y-time-series1', 'figure'),
    dash.dependencies.Input('country1', 'value'),
    dash.dependencies.Input('country2', 'value')
)
##Different code to find min,max values
def update_charts(country1, country2):
    filtered_df = df_flat.loc[df_flat['Country Name'] == country1]

    CO2_df = filtered_df.loc[filtered_df['Series Name'] == 'Methane emissions (kt of CO2 equivalent)']
    maxv = CO2_df.nlargest(1, 'value')['value'].values.tolist()
    minv = CO2_df.nsmallest(1, 'value')['value'].values.tolist()

    filtered_df2 = df_flat.loc[df_flat['Country Name'] == country2]
    CO2_df2 = filtered_df2.loc[filtered_df2['Series Name'] == 'Methane emissions (kt of CO2 equivalent)']

    maxv2 = CO2_df2.nlargest(1, 'value')['value'].values.tolist()
    minv2 = CO2_df2.nsmallest(1, 'value')['value'].values.tolist()

    maxva2 = max(maxv + maxv2)
    minva2 = min(minv + minv2)

    figure1 = px.line(CO2_df, x='Year', y='value', title='Methane emissions (kt of CO2 equivalent)',
                      range_y=[minva2, maxva2])
    figure2 = px.line(CO2_df2, x='Year', y='value', title='Methane emissions (kt of CO2 equivalent)',
                      range_y=[minva2, maxva2])
    return figure1, figure2


if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)
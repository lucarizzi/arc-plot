import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import os

import pandas as pd
import plotly.graph_objs as go

import numpy as np
from scipy.ndimage.filters import gaussian_filter

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# SETUP THE DATA STRUCTURES and READ LINE LISTS

directory = "arcplots"

sides = ["red", "blue"]

dichroics = {
    '460': {'file': 'dichroic_460_t.dat'},
    '500': {'file': 'dichroic_500_t.dat'},
    '560': {'file': 'dichroic_560_t.dat'},
    '680': {'file': 'dichroic_680_t.dat'}
}


gratings = dict()

gratings["150/7500"] = {
        "dispersion": 3,
        "range": 12288,
        "id": "150/7500"}

gratings["300/5000"] = {
        "dispersion": 1.59,
        "range": 6525,
        "id": "300/5000"}

gratings["400/8500"] = {
        "dispersion": 1.16,
        "range": 4762,
        "id": "400/8500"}

gratings["600/7500"] = {
        "dispersion": 0.80,
        "range": 3275,
        "id": "600/7500"}

gratings["600/5000"] = {
        "dispersion": 0.80,
        "range": 3275,
        "id": "600/5000"}

gratings["600/10000"] = {
        "dispersion": 0.80,
        "range": 3275,
        "id": "600/10000"}

gratings["831/8200"] = {
        "dispersion": 0.58,
        "range": 2375,
        "id": "831/8200"}

# convert into a pandas data source

# use the line list on disk to populate the Pandas data frame

line_list_file = os.path.join(directory,'lamps.dat')
line_list = pd.read_csv(line_list_file, delim_whitespace=True)
line_list.columns = ['Wavelength', 'Hg', 'Ne', 'Ar', 'Zn', 'Cd']

for key in dichroics.keys():
    df = pd.read_csv(os.path.join(directory, dichroics[key]['file']), delim_whitespace=True)
    df.columns = ['wavelength', 'transmission']
    transmission = np.interp(line_list.Wavelength, df.wavelength, df.transmission)
    dichroics[key]['transmission'] = transmission

print(dichroics)

dropdown_options_for_gratings = []
for grating in gratings.keys():
    option = {}
    option['label'] = grating
    option['value'] = grating
    dropdown_options_for_gratings.append(option)

dropdown_options_for_dichroics = []
for dichroic in dichroics.keys():
    option = {}
    option['label'] = dichroic
    option['value'] = dichroic
    dropdown_options_for_dichroics.append(option)

app.layout = html.Div([
        html.Div([
            html.H3('Red side grating'),
            dcc.Dropdown(
                id='id-select-grating',
                options=dropdown_options_for_gratings,
                value='600/10000'
                    ),
            html.H3('Central wavelength'),
            dcc.Input(
                id='id-central-wavelength',
                type='text',
                value=5500
                    ),
            html.H3('Dichroic'),
            dcc.Dropdown(
                id='id-select-dichroic',
                options=dropdown_options_for_dichroics,
                value='560'
                    ),
            ],
            style={'width': '49%', 'display': 'inline-block'}
        ),
        dcc.Graph(
            id='id-red-side-arcplot',
            style = {'width': '49%'}
        ),
        html.Div(id='id-range')

])

@app.callback(
    Output(component_id='id-range', component_property='children'),
    [Input(component_id='id-select-grating', component_property='value')]
)
def update_range_div(value):
    range = gratings[value]['range']
    return 'Wavelength range for this grating: {}'.format(range)


@app.callback(
    Output(component_id='id-red-side-arcplot', component_property='figure'),
    [Input(component_id='id-central-wavelength', component_property='value'),
     Input(component_id='id-select-grating', component_property='value'),
     Input(component_id='id-select-dichroic', component_property='value')],
)
def update_figure_xrange(central_wavelength, grating, dichroic):
    range=gratings[grating]['range']
    try:
        xmin = float(central_wavelength)-(range/2)
        xmax = float(central_wavelength)+(range/2)
    except ValueError:
        xmin=3700
        xmax=9000
    if xmin<3000:
        xmin = 3000
    if xmax>11000:
        xmax = 11000
    line_plot_data = []
    lamps = list(line_list)
    for lamp in lamps[1:]:
        line_plot_data.append(
            {
                'x': line_list['Wavelength'],
                'y': gaussian_filter(line_list[lamp]*dichroics[dichroic]['transmission'], sigma=4),
                'name': str(lamp),
                'mode': 'lines'

            }
        )

    arcplot_figure = {
                'data': line_plot_data,
                'layout': {
                    'clickmode': 'event+select',
                    'xaxis': {'range': [xmin,xmax]}
                    }

        }
    return arcplot_figure



if __name__ == '__main__':
    app.run_server(debug=True)
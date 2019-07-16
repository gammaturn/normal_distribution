# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import numpy as np
import scipy.stats

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.title = "Normal distribution"

# global variables
x_max = 5.
n_points = 150
x = np.linspace(-x_max, x_max, n_points)

pdf_std = go.Scatter(
    x=x,
    y=scipy.stats.norm.pdf(x, scale=1.0),  # standard normal distribution
    mode='lines',
    name='standard normal<br>distribution',
    showlegend=False,
    line={'dash': 'dash', 'width': 1.5}
)
cdf_std = go.Scatter(
    x=x,
    y=scipy.stats.norm.cdf(x, scale=1.0),  # cdf of standard normal distribution
    mode='lines',
    name='standard normal<br>distribution',
    showlegend=False,
    line={'dash': 'dash', 'width': 1.5}
)

# components of the app
pdf_display = html.Div(dcc.Graph(id='pdf-display'), className='six columns')

cdf_display = html.Div(dcc.Graph(id='cdf-display'), className='six columns')

slider = html.Div([
    html.Label('Use the slider to set the standard deviation of the normal distribution:'),
    dcc.Slider(
        id='sigma-slider',
        min=5, max=30, step=1,
        marks={i: '{:.1f}'.format(i / 10) for i in range(5, 31, 5)},
        value=10
    ),
], className="six columns offset-by-three")

app.layout = html.Div([
    html.Div([
        html.H1('Normal Distribution', className="app-header--title"),
        html.A(html.Img(src='/assets/gammaturn.png', className="app-header--image"),
               href="https://github.com/gammaturn/normal_distribution")
    ],
        className="app-header"
    ),
    html.Div([pdf_display, cdf_display], className='row'),
    html.Div(slider, className='row')
], className = "ten columns offset-by-one"
)


@app.callback(
    [Output('pdf-display', 'figure'),
     Output('cdf-display', 'figure')],
    [Input('sigma-slider', 'value')]
)
def create_figures(sigma):
    pdf_var = go.Scatter(
        x=x,
        y=scipy.stats.norm.pdf(x, scale=sigma / 10.),
        mode='lines',
        name='normal distribution<br>(sigma={:.1f})'.format(sigma / 10.),
        showlegend=False,
        line={'dash': 'solid', 'width': 3}
    )
    cdf_var = go.Scatter(
        x=x,
        y=scipy.stats.norm.cdf(x, scale=sigma / 10.),
        mode='lines',
        name='normal distribution<br>(sigma={:.1f})'.format(sigma / 10.),
        showlegend=False,
        line={'dash': 'solid', 'width': 3}
    )

    return (go.Figure(data=[pdf_std, pdf_var],
                      layout={
                          'xaxis': {'title': {'text': 'random variable'}},
                          'yaxis': {'title': {'text': 'pdf'}},
                          'margin': {'t': 50, 'b': 80, 'l': 20, 'r': 20},
                          'template': 'ggplot2',
                          'colorway': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
                                       '#ff7f00', '#ffff33', '#a65628', '#f781bf',
                                       '#999999']
                      }),
            go.Figure(data=[cdf_std, cdf_var],
                      layout={
                          'xaxis': {'title': {'text': 'random variable'}},
                          'yaxis': {'title': {'text': 'cdf'}},
                          'margin': {'t': 50, 'b': 80, 'l': 50, 'r': 20},
                          'template': 'ggplot2',
                          'colorway': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
                                       '#ff7f00', '#ffff33', '#a65628', '#f781bf',
                                       '#999999']
                      })
            )


if __name__ == '__main__':
    app.run_server(debug=True)

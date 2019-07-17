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

sigma_min = 5
sigma_max = 30
pdfs = {i: scipy.stats.norm.pdf(x, scale=i/10.) for i in range(sigma_min, sigma_max+1)}
cdfs = {i: scipy.stats.norm.cdf(x, scale=i/10.) for i in range(sigma_min, sigma_max+1)}

pdf_std = go.Scatter(
    x=x,
    y=pdfs[10],  # standard normal distribution, scipy.stats.norm.pdf(x, scale=1.0)
    mode='lines',
    name='standard normal<br>distribution',
    showlegend=True,
    line={'dash': 'dash', 'width': 1.5}
)
cdf_std = go.Scatter(
    x=x,
    y=cdfs[10],  # cdf of standard normal distribution, scipy.stats.norm.cdf(x, scale=1.0)
    mode='lines',
    name='standard normal<br>distribution',
    showlegend=True,
    line={'dash': 'dash', 'width': 1.5}
)

# components of the app
pdf_display = html.Div(dcc.Graph(id='pdf-display'), className='six columns')

cdf_display = html.Div(dcc.Graph(id='cdf-display'), className='six columns')

slider = html.Div([
    html.Label('Use the slider to set the standard deviation of the normal distribution:'),
    dcc.Slider(
        id='sigma-slider',
        min=sigma_min, max=sigma_max, step=1,
        marks={i: '{:.1f}'.format(i / 10) for i in range(5, sigma_max+1, 5)},
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
], className="ten columns offset-by-one"
)


@app.callback(
    Output('cdf-display', 'figure'),
    [Input('sigma-slider', 'value')]
)
def create_cdf(sigma):
    cdf_var = go.Scatter(
        x=x,
        y=cdfs[sigma],  # scipy.stats.norm.cdf(x, scale=sigma / 10.),
        mode='lines',
        name='normal distribution<br>(sigma={:.1f})'.format(sigma / 10.),
        showlegend=True,
        line={'dash': 'solid', 'width': 3}
    )

    return go.Figure(data=[cdf_std, cdf_var],
                     layout={
                         'xaxis': {'title': {'text': 'random variable'}},
                         'yaxis': {'title': {'text': 'cdf'}},
                         'margin': {'t': 50, 'b': 80, 'l': 50, 'r': 20},
                         'template': 'ggplot2',
                         'colorway': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
                                      '#ff7f00', '#ffff33', '#a65628', '#f781bf',
                                      '#999999'],
                         'legend': {'xanchor': 'right', 'yanchor': 'bottom', 'x': 1, 'y': 0.05}
                     })


@app.callback(
    Output('pdf-display', 'figure'),
    [Input('sigma-slider', 'value'),
     Input('cdf-display', 'clickData')]
)
def create_pdf(sigma, clickdata):
    pdf_var = go.Scatter(
        x=x,
        y=pdfs[sigma],  # scipy.stats.norm.pdf(x, scale=sigma / 10.),
        mode='lines',
        name='normal distribution<br>(sigma={:.1f})'.format(sigma / 10.),
        showlegend=True,
        line={'dash': 'solid', 'width': 3}
    )

    data = [pdf_std, pdf_var]

    if clickdata is not None:
        if clickdata['points'][0]['curveNumber'] == 1:
            index = clickdata['points'][0]['pointIndex']
            xval = clickdata['points'][0]['x']
            data.append(go.Scatter(
                x=x[:index+1],
                y=pdfs[sigma][:index+1],
                mode='none',
                showlegend=False,
                fill='tozeroy',
                hoveron='fills',
                text='area: {:.3f}'.format(scipy.stats.norm.cdf(xval, scale=sigma/10.)),
                hoverinfo='text'
            ))

    return go.Figure(data=data,
                     layout={
                         'xaxis': {'title': {'text': 'random variable'}},
                         'yaxis': {'title': {'text': 'pdf'}},
                         'margin': {'t': 50, 'b': 80, 'l': 20, 'r': 20},
                         'template': 'ggplot2',
                         'colorway': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
                                      '#ff7f00', '#ffff33', '#a65628', '#f781bf',
                                      '#999999'],
                         'legend': {'xanchor': 'right', 'yanchor': 'top', 'x': 1, 'y': 1}
                      })


if __name__ == '__main__':
    app.run_server(debug=True)

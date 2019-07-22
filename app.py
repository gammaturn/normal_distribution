# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go

import numpy as np
import scipy.stats

app = dash.Dash(__name__)

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
pdf_display = html.Div([dcc.Graph(id='pdf-display')], className='pretty_container six columns')

cdf_display = html.Div([dcc.Graph(id='cdf-display')], className='pretty_container six columns')

slider = html.Div([
    html.P('Use the slider to set the standard deviation of the normal distribution:',
           className="control_label"),
    dcc.Slider(
        id='sigma-slider',
        min=sigma_min, max=sigma_max, step=1,
        marks={i: '{:.1f}'.format(i / 10) for i in range(5, sigma_max+1, 5)},
        value=10,
        className="dcc_control"
    ),
], className="pretty_container six columns offset-by-three")

app.layout = html.Div([
    html.Div([
        html.H1('Normal Distribution', className="ten columns"),
        html.Div([
            html.A(html.Img(src='/assets/gammaturn.png',
                            style={'position': 'relative',
                                   'vertical-align': 'middle',
                                   'display': 'inline',
                                   'float': 'right',
                                   'height': '70px'}),
                   href="https://github.com/gammaturn/normal_distribution")
        ], className="two columns")
    ],
        className="row flex-display"
    ),
    html.Div([pdf_display, cdf_display], className='row flex-display'),
    html.Div(slider, className='row flex-display')
], style={"display": "flex", "flex-direction": "column"}
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
                         'margin': {'t': 60, 'b': 20, 'l': 10, 'r': 10},
                         'template': 'ggplot2',
                         'colorway': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
                                      '#ff7f00', '#ffff33', '#a65628', '#f781bf',
                                      '#999999'],
                         'legend': {'xanchor': 'right', 'yanchor': 'bottom', 'x': 1, 'y': 0.05},
                         'title': go.layout.Title(text="Cumulative distribution function", xref="paper", x=0)
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
                         'margin': {'t': 60, 'b': 20, 'l': 10, 'r': 10},
                         'template': 'ggplot2',
                         'colorway': ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3',
                                      '#ff7f00', '#ffff33', '#a65628', '#f781bf',
                                      '#999999'],
                         'legend': {'xanchor': 'right', 'yanchor': 'top', 'x': 1, 'y': 1},
                         'title': go.layout.Title(text="Probability density function", xref="paper", x=0)
                     })


if __name__ == '__main__':
    app.run_server(debug=True)

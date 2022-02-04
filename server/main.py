import dash
import dash_bootstrap_components as dbc

from dash import dcc
from dash import html

import dash_draggable


from widgets import dropdown, create_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([
    dcc.Interval(
        id='interval-component',
        interval=100,  # in milliseconds
        n_intervals=0
    ),

    html.H1("Dash Telemetry Demo"),
    html.Div(id="test"),
    dropdown,

    dash_draggable.GridLayout(
        id='draggable',
        clearSavedLayout=True,
        children=[

            dcc.Slider(
                id='slider',
                min=0,
                max=4,
                value=0,
                marks={str(year): str(year) for year in range(5)},
                step=None),
        ]
    ),

])

create_callbacks(app)


if __name__ == '__main__':
    app.run_server(debug=True, port=5080)


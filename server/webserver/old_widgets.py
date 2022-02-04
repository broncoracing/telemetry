import math

import dash

import dash_bootstrap_components as dbc
from dash import dcc
import dash_daq as daq
from dash import Input, Output, html, State, ALL
from dash.exceptions import PreventUpdate

import uuid

import plotly.express as px

import pandas as pd

graph_data = pd.DataFrame(columns=("x", "y"))


def create_slider():
    random_id = str(uuid.uuid4())
    slider = html.Span(dcc.Slider(
            id={'type': "Slider", 'index': random_id},
            min=0,
            max=4,
            value=0,
            marks={str(year): str(year) for year in range(5)},
            step=None
        ),
        id=random_id
    )
    return slider


def create_gauge():
    random_id = str(uuid.uuid4())
    gauge = html.Span(daq.Gauge(
            id={'index': random_id, 'type': "Gauge"},
            label="Sin(t)",

            min=-1,
            max=1,
            value=0
        ),
        id=random_id
    )

    return gauge


def create_graph():
    random_id = str(uuid.uuid4())
    gauge = html.Span(dcc.Graph(
            id={'index': random_id, 'type': "Graph"},
            responsive=True,
            style={
                "width": "100%",
                "height": "100%",
            }
        ),
        id=random_id
    )

    return gauge


addable_components = {
    "Slider": create_slider,
    "Gauge": create_gauge,
    "Graph": create_graph,
}

ADD_DROPDOWN_PREFIX = "add_dropdown_"


dropdown = dbc.DropdownMenu(
    label="Add item",
    children=[
        dbc.DropdownMenuItem(name, id={'type': ADD_DROPDOWN_PREFIX, 'index': name}, n_clicks=0) for name in addable_components.keys()
    ],
    direction="end"
)


def create_callbacks(app):
    @app.callback(
        Output("draggable", "children"),
        Input({'type': ADD_DROPDOWN_PREFIX, 'index': ALL}, 'n_clicks'),
        State("draggable", "children"),
    )
    def add_element(n, children):
        if all(val == 0 for val in n):
            raise PreventUpdate

        ctx = dash.callback_context

        if not ctx.triggered:
            button_id = 'No clicks yet'
        else:
            button_id = ctx.triggered[0]['prop_id'].split('"')[3]

        # print(button_id)

        new_item = addable_components[button_id]()
        children.append(new_item)
        return children


    @app.callback(
        Output({'type': "Gauge", 'index': ALL}, 'value'),
        Input('interval-component', 'n_intervals'),
    )
    def guage_callback(n):

        ctx = dash.callback_context

        return [math.sin(n * 0.1)] * len(ctx.outputs_list)

    @app.callback(
        Output({'type': "Graph", 'index': ALL}, 'figure'),
        Input('interval-component', 'n_intervals'),
        Input('slider', 'value'),
    )
    def graph_callback(n, s):
        global graph_data
        graph_data = graph_data.append({"x":n * 0.1, "y":math.sin(n * 0.1) + s}, ignore_index=True)
        # print(graph_data)
        ctx = dash.callback_context
        fig = px.line(graph_data.tail(50), "x", "y")

        # fig.update_layout(transition_duration=50)
        return [fig] * len(ctx.outputs_list)


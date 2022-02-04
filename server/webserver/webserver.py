import dash
import dash_bootstrap_components as dbc

from dash import dcc
from dash import html

import dash_draggable

# from .old_widgets import dropdown, create_callbacks
from .widgets import create_widget_callbacks
from .create_widget_dropdown import create_dropdown_callback, dropdown


class Webserver:
    def __init__(self, debug, port):
        self.debug = debug
        self.port = port

        # Initialize app
        # prevent_initial_callbacks=True prevents the update callbacks from being called on creation
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], prevent_initial_callbacks=True)

        # Create the app layout
        self.app.layout = dbc.Container([
            # Interval component periodically triggers callbacks. TODO: Make this use websockets instead
            dcc.Interval(
                id='interval-component',
                interval=1000,  # in milliseconds
                n_intervals=0
            ),

            # Stores json data of the raw telemetry data. This will be updated via websockets.
            dcc.Store(id='telemetry_data'),


            html.H1("Telemetry Dashboard"),
            # html.Div(id="test"),
            dropdown,
            # Grid layout contains all of the resizable/movable components.
            dash_draggable.GridLayout(
                id='draggable',
                clearSavedLayout=True,
                children=[]
            ),

        ])

        # Create the necessary callbacks
        create_dropdown_callback(self.app)
        create_widget_callbacks(self.app)

    def run(self):
        self.app.run_server(debug=self.debug, port=self.port)


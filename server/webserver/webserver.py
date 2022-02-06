import dash
import dash_bootstrap_components as dbc
from dash.dependencies import ClientsideFunction, Input, Output, State
from dash import html, dcc
import dash_websocket

import dash_draggable

from .widgets import create_widget_callbacks
from .widget_callbacks import create_widget_management_callbacks, dropdown


class Webserver:
    def __init__(self, debug, port):
        self.debug = debug
        self.port = port

        # Initialize app
        # prevent_initial_callbacks=True prevents the update callbacks from being called on creation
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI], prevent_initial_callbacks=True, update_title=None)
        self.app.title = 'Bronco Racing Telemetry'
        # Create the app layout
        self.app.layout = html.Div([
            # Stores data of the raw telemetry data. This will be updated via websockets.
            dcc.Store(id='telemetry_data'),
            # Stores the data column headers but not the data itself. This is used to update dropdowns/settings.
            dcc.Store(id='telemetry_data_columns'),

            # Navbar on top holds logo/heading, and buttons/links to add stuff or save/load.
            dbc.Navbar(
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=self.app.get_asset_url('logo.png'), height="30px")),
                                dbc.Col(dbc.NavbarBrand("Telemetry Dashboard", className="ms-2")),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                        dbc.Collapse(
                            dropdown,
                            id="navbar-collapse",
                            is_open=False,
                            navbar=True,
                        ),
                    ]
                ),
                color="dark",
                dark=True,
            ),

            dash_websocket.DashWebsocket(id='ws', url='ws://127.0.0.1:5678'),  # woohoo custom component!



            # Grid layout contains all of the resizable/movable components.
            dash_draggable.ResponsiveGridLayout(
                id='draggable',
                clearSavedLayout=True,
                children=[],
                gridCols={'lg': 21, 'md': 17, 'sm': 14, 'xs': 7, 'xxs': 5}
            ),

        ])

        # Create the necessary callbacks
        create_widget_management_callbacks(self.app)
        create_widget_callbacks(self.app)

        self.app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_data_from_websockets'
            ),
            [Output("telemetry_data", "data"),
             Output("telemetry_data_columns", "data")],
            [Input('ws', 'msg')],
            [State("telemetry_data", "data"),
             State("telemetry_data_columns", "data")]
        )

    def run(self):
        self.app.run_server(debug=self.debug, port=self.port)


import dash
import dash_bootstrap_components as dbc
from dash.dependencies import ClientsideFunction, Input, Output, State, ALL
from dash import html, dcc
import dash_websocket

import dash_draggable
from dash.development.base_component import Component
from dash.exceptions import PreventUpdate

from . import persistence
from .persistence import save_layout, get_saves
from .widgets import create_widget_callbacks, telemetry_widgets
from .widget_callbacks import create_widget_management_callbacks, dropdown

from pathlib import Path

import datetime
import functools

import json


class Webserver:
    def __init__(self, debug, port, save_dir):
        self.debug = debug
        self.port = port
        self.save_dir = Path(save_dir)

        # Initialize app
        # prevent_initial_callbacks=True prevents the update callbacks from being called on creation
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.YETI], prevent_initial_callbacks=True,
                             update_title=None)
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
                                dbc.Col(
                                    dbc.Badge("Not saved", color="warning", className="me-1", id='saved-indicator')),
                            ],
                            align="center",
                            className="g-0",
                        ),
                        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                        dbc.Collapse(
                            dbc.Row(
                                [
                                    dbc.Col(dropdown),
                                    dbc.Col(dbc.NavLink("Save layout", href="#", id="open_save_layout", n_clicks=0, ),
                                            width='auto'),
                                    dbc.Col(dbc.NavLink("Load layout", href="#", id="open_load_layout", n_clicks=0, ),
                                            width='auto'),
                                ],
                                className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
                                align="center",
                            ),
                            id="navbar-collapse",
                            is_open=False,
                            navbar=True,
                        ),
                    ]
                ),
                color="dark",
                dark=True,
            ),

            dash_websocket.DashWebsocket(id='ws', port='5678'),  # woohoo custom component!

            # Grid layout contains all of the resizable/movable components.
            dash_draggable.ResponsiveGridLayout(
                id='draggable',
                save=False,
                children=persistence.load_widgets(self.save_dir, 'default') if 'default' in persistence.get_saves(self.save_dir) else [],
                layouts=persistence.load_layouts(self.save_dir, 'default') if 'default' in persistence.get_saves(self.save_dir) else {},
                gridCols={'lg': 21, 'md': 17, 'sm': 14, 'xs': 7, 'xxs': 5},
            ),
            dcc.Store(id='dummy_after_load', data=None),

            # Lists filenames to save
            html.Datalist(
                id='suggested-save-names',
                children=[]
            ),

            # Modal dialog for saving layout
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Save layout")),
                    dbc.ModalBody(dbc.Container([
                        dbc.Row("Choose a name for the saved layout:"),
                        dbc.Row([
                            dbc.Col(dcc.Input(id='save_filename', type='text', list='suggested-save-names', value=''),
                                    width='auto'),
                            dbc.Col(dbc.Button("Save", color="success", className="me-1", id='save_layout', )),
                            html.Span(id='save_callback_placeholder')
                        ], align="center", )
                    ])),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close_save_layout", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="save_layout_modal",
                is_open=False,
            ),
            # Modal dialog for loading layout
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Load layout")),
                    dbc.ModalBody(dbc.Container([
                        dbc.DropdownMenu(
                            label="Choose a layout to load",
                            children=[],
                            id='load-dropdown'
                        )
                    ])),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close_load_layout", className="ms-auto", n_clicks=0
                        )
                    ),
                ],
                id="load_layout_modal",
                is_open=False,
            ),
        ])

        # Create the necessary callbacks
        create_widget_management_callbacks(self.app, self.save_dir)
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

        # add callback for toggling the collapse on small screens
        @self.app.callback(
            Output("navbar-collapse", "is_open"),
            [Input("navbar-toggler", "n_clicks")],
            [State("navbar-collapse", "is_open")],
        )
        def toggle_navbar_collapse(n, is_open):
            if n:
                return not is_open
            return is_open

        @self.app.callback(
            Output("save_layout_modal", "is_open"),
            [Input("open_save_layout", "n_clicks"), Input("close_save_layout", "n_clicks")],
            [State("save_layout_modal", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

        @self.app.callback(
            Output("load_layout_modal", "is_open"),
            [Input("open_load_layout", "n_clicks"), Input("close_load_layout", "n_clicks")],
            [State("load_layout_modal", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

        @self.app.callback(
            [Output('suggested-save-names', 'children'), Output('load-dropdown', 'children')],
            [Input("open_load_layout", "n_clicks"), Input("open_save_layout", "n_clicks")]
        )
        def update_filenames(n1, n2):
            saves = get_saves(self.save_dir)
            return [
                [html.Option(value=word) for word in saves],
                [dbc.DropdownMenuItem(word, id={'index': 'load_layout-' + word, 'type': 'load-option'}) for word in saves]
            ]

        @self.app.callback(
            [Output('saved-indicator', 'color'),
             Output('saved-indicator', 'children'),
             Output('save_callback_placeholder', 'children')],
            Input("save_layout", "n_clicks"),
            [
                State('save_filename', 'value'),
                State('draggable', 'layouts')
            ] + [State({'type': widget_cls.get_widget_data_type(), 'index': ALL}, "data") for widget_cls in
                 telemetry_widgets.values()],
        )
        def save(n, save_filename, layouts, *widget_configs):
            if not n:
                raise PreventUpdate

            if not layouts or save_filename == '':
                return ['danger', 'Failed to save: No data',
                        dbc.Badge("Failed to save", color="danger", className="me-1")]

            configs = functools.reduce(lambda a, b: a + b, widget_configs)

            save_layout(layouts, configs, self.save_dir, save_filename)

            return ['primary', 'Saved {}'.format(datetime.datetime.now().strftime('%I:%M %p')), '']

        @self.app.callback(
            Output('save_filename', 'value'),
            Input({'type': 'load-option', 'index': ALL}, 'n_clicks')
        )
        def update_save_filename_on_load(name):
            ctx = dash.callback_context
            if not ctx.triggered:
                raise PreventUpdate
            else:
                # Get the id of the clicked button. This is the type of the widget to create.
                button_id = ctx.triggered[0]['prop_id'].split('"')[3]
                # print(button_id)
                return button_id[12:]

    def run(self):
        if self.debug:
            # Run on localhost with debug setting turned on
            self.app.run_server(debug=True, port=self.port)
        else:
            # run with host 0.0.0.0 and debug turned off
            self.app.run_server(host='0.0.0.0', debug=False, port=self.port)


import math
import pandas as pd
from dash import ClientsideFunction, MATCH

from .base_widget import *


class Graph(BaseWidget):
    widget_name = "Graph"
    widget_type = "Graph"

    def __init__(self, saved_data=None):
        super().__init__(saved_data)

    def create_widget(self):
        return dcc.Graph(
            id=self.widget_id,
            responsive=True,
            style={
                "width": "100%",
                "height": "100%",
            },
            # figure=px.line(pd.DataFrame(columns=("timestamp", "float data")), "timestamp", "float data")
        )

    def create_settings_menu(self):
        return [
            html.Div(
                [
                    'Graph title:',
                    dcc.Input(type='text', placeholder='Enter title...', value='',
                              id={'index': self.random_id, 'type': 'graph_title_input'})
                ]
            ),
            html.Div(
                [
                    'Data sources:',
                    dcc.Dropdown(id={'index': self.random_id, 'type': 'graph_axis_dropdown'}, multi=True)
                ]
            ),
            html.Div([
                'Persistence:',
                daq.NumericInput(
                    id={'index': self.random_id, 'type': 'graph_persistence'},
                    min=1, max=600, value=30
                ),
                ' Seconds'
            ]),
            html.Div([
                'Max data points:',
                daq.NumericInput(
                    id={'index': self.random_id, 'type': 'graph_max_points'},
                    min=1, max=10000, value=2000
                ),
            ]),
            html.Div(
                [
                    'Line style:',
                    dcc.Dropdown(
                        options=[
                            {'label': 'Line only', 'value': 'lines'},
                            {'label': 'Points only', 'value': 'markers'},
                            {'label': 'Points and line', 'value': 'lines+markers'},
                        ],
                        value='line',
                        id={'index': self.random_id, 'type': 'graph_line_style'}
                    )
                ]
            )]

    @classmethod
    def create_callback(cls, app):
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_graph_from_data'
            ),
            Output({'type': "Graph", 'index': MATCH}, 'figure'),
            [Input('telemetry_data', 'data'),
             Input({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')],
            State({'type': "Graph", 'index': MATCH}, 'figure')
        )


        @app.callback(
            Output({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data'),
            [Input({'type': "graph_title_input", 'index': MATCH}, 'value'),
             Input({'type': "graph_axis_dropdown", 'index': MATCH}, 'value'),
             Input({'type': "graph_persistence", 'index': MATCH}, 'value'),
             Input({'type': "graph_max_points", 'index': MATCH}, 'value'),
             Input({'type': "graph_line_style", 'index': MATCH}, 'value')],
            State({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')
        )
        def update_settings(title, axes, persistence, max_points, line_style, data):
            if title is None:
                title = ''
            if axes is None:
                axes = []
            if persistence is None:
                persistence = 30
            if max_points is None:
                max_points = 2000
            if line_style is None:
                line_style = 'lines'

            data['title'] = title
            data['axes'] = axes
            data['persistence'] = persistence
            data['max_points'] = max_points
            data['line_style'] = line_style

            return data

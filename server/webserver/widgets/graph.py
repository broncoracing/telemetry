import math
import pandas as pd
from dash import ClientsideFunction, MATCH

from .base_widget import *


class Graph(BaseWidget):
    widget_name = "Graph"
    widget_type = "Graph"

    def __init__(self):
        super().__init__()

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
        return self._source_settings_menu()

    @staticmethod
    def create_callback(app):
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_graph_from_data'
            ),
            Output({'type': "Graph", 'index': ALL}, 'figure'),
            Input('telemetry_data', 'data'),
            State({'type': "Graph", 'index': ALL}, 'figure')
        )


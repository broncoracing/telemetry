import math
import pandas as pd

from .base_widget import *


class Slider(BaseWidget):
    widget_name = "Graph testname"
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
            }
        )

    @staticmethod
    def create_callback(app):
        @app.callback(
            Output({'type': "Graph", 'index': ALL}, 'figure'),
            Input('interval-component', 'n_intervals'),
        )
        def graph_callback(n):
            graph_data = pd.DataFrame(columns=("x", "y"))
            print(n)
            for i in range(n):
                graph_data = graph_data.append({"x":i * 0.1, "y":math.sin(i * 0.1)}, ignore_index=True)

            print(graph_data)
            ctx = dash.callback_context
            fig = px.line(graph_data, "x", "y")

            # fig.update_layout(transition_duration=50)
            return [fig] * len(ctx.outputs_list)

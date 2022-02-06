from dash import ClientsideFunction, MATCH

from .base_widget import *
import dash_daq as daq


class Gauge(BaseWidget):
    widget_name = "Gauge"
    widget_type = "Gauge"

    def __init__(self):
        super().__init__()

    def create_widget(self):
        return daq.Gauge(
            id=self.widget_id,
            showCurrentValue=True,
            label='No source',
            min=0,
            max=10,
            value=0,
            color="#FF5E5E"
        )

    def create_settings_menu(self):
        return [
            self._source_settings_menu(),
            html.Div([
                'Minimum value:',
                daq.NumericInput(
                    id={'index': self.random_id, 'type': 'gauge_min_value'},
                    value=0, min=-999999, max=999999
                ),
            ]),
            html.Div([
                'Maximum value:',
                daq.NumericInput(
                    id={'index': self.random_id, 'type': 'gauge_max_value'},
                    value=10, min=-999999, max=999999
                ),
            ])
        ]

    @staticmethod
    def create_callback(app):
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_thermometer_widget'
            ),
            [Output({'type': "Gauge", 'index': ALL}, 'value'),
             Output({'type': "Gauge", 'index': ALL}, 'max'),
             Output({'type': "Gauge", 'index': ALL}, 'min')],
            [Input('telemetry_data', 'data'),
             Input({'type': "gauge_max_value", 'index': ALL}, 'value'),
             Input({'type': "gauge_min_value", 'index': ALL}, 'value')],
            [State({'type': "Gauge", 'index': ALL}, 'label')]
        )

        # Data source changed
        @app.callback(
            Output({'type': Gauge.widget_type, 'index': MATCH}, 'label'),
            Input({'type': 'value_dropdown', 'index': MATCH}, 'value')
        )
        def select_data_source(val):
            if val is None:
                return 'No source'
            return val
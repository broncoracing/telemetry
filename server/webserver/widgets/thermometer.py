from dash import ClientsideFunction, MATCH

from .base_widget import *
import dash_daq as daq


class Thermometer(BaseWidget):
    widget_name = "Thermometer"
    widget_type = "Thermometer"

    def __init__(self):
        super().__init__()

    def create_widget(self):
        return daq.Thermometer(
            id=self.widget_id,
            showCurrentValue=True,
            label='No source',
            min=0,
            max=10,
            value=0,
            width=5,
            color="#FF5E5E"
        )

    def create_settings_menu(self):
        return [
            self._source_settings_menu(),
            html.Div([
                'Minimum value:',
                daq.NumericInput(
                    id={'index': self.random_id, 'type': 'thermometer_min_value'},
                    min=-999999, max=999999, value=0
                ),
            ]),
            html.Div([
                'Maximum value:',
                daq.NumericInput(
                    id={'index': self.random_id, 'type': 'thermometer_max_value'},
                    min=-999999, max=999999, value=10
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
            [Output({'type': "Thermometer", 'index': ALL}, 'value'),
             Output({'type': "Thermometer", 'index': ALL}, 'max'),
             Output({'type': "Thermometer", 'index': ALL}, 'min')],
            [Input('telemetry_data', 'data'),
             Input({'type': "thermometer_max_value", 'index': ALL}, 'value'),
             Input({'type': "thermometer_min_value", 'index': ALL}, 'value')],
            [State({'type': "Thermometer", 'index': ALL}, 'label')]
        )

        # Data source changed
        @app.callback(
            Output({'type': Thermometer.widget_type, 'index': MATCH}, 'label'),
            Input({'type': 'value_dropdown', 'index': MATCH}, 'value')
        )
        def select_data_source(val):
            if val is None:
                return 'No source'
            return val


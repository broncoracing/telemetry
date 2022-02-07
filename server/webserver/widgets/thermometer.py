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

    @classmethod
    def create_callback(cls, app):
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_thermometer_widget'
            ),
            [Output({'type': "Thermometer", 'index': MATCH}, 'value'),
             Output({'type': "Thermometer", 'index': MATCH}, 'max'),
             Output({'type': "Thermometer", 'index': MATCH}, 'min'),
             Output({'type': "Thermometer", 'index': MATCH}, 'label')
             ],
            [Input('telemetry_data', 'data'),
             Input({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')],
        )

        # Data source changed
        @app.callback(
            [Output({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')],
            [Input({'type': 'value_dropdown', 'index': MATCH}, 'value'),
             Input({'type': 'thermometer_min_value', 'index': MATCH}, 'value'),
             Input({'type': 'thermometer_max_value', 'index': MATCH}, 'value')],
            [State({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')]
        )
        def update_settings(value, scale_min, scale_max, data):
            print(data)

            if value is None:
                value = 'No source'
            if scale_min is None:
                scale_min = 0
            if scale_max is None:
                scale_max = 10

            data['value'] = value
            data['min'] = scale_min
            data['max'] = scale_max

            return [data]



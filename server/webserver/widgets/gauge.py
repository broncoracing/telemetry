from dash import ClientsideFunction, MATCH

from .base_widget import *
import dash_daq as daq


class Gauge(BaseWidget):
    widget_name = "Gauge"
    widget_type = "Gauge"

    def __init__(self, saved_data=None):
        super().__init__(saved_data)

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

    @classmethod
    def create_callback(cls, app):
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_thermometer_widget'
            ),
            [Output({'type': "Gauge", 'index': MATCH}, 'value'),
             Output({'type': "Gauge", 'index': MATCH}, 'max'),
             Output({'type': "Gauge", 'index': MATCH}, 'min'),
             Output({'type': "Gauge", 'index': MATCH}, 'label')
             ],
            [Input('telemetry_data', 'data'),
             Input({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')],
        )

        # Data source changed
        @app.callback(
            [Output({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')],
            [Input({'type': 'value_dropdown', 'index': MATCH}, 'value'),
             Input({'type': 'gauge_min_value', 'index': MATCH}, 'value'),
             Input({'type': 'gauge_max_value', 'index': MATCH}, 'value')],
            [State({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data'),
             State({'type': 'settings_btn', 'index': MATCH}, 'n_clicks')]
        )
        def update_settings(value, scale_min, scale_max, data, settings_clicks):
            if settings_clicks is None or settings_clicks == 0:
                raise PreventUpdate
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

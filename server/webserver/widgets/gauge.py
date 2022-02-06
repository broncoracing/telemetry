from dash import ClientsideFunction

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
            label='int data',
            min=0,
            max=10,
            value=0,
        )

    @staticmethod
    def create_callback(app):
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_thermometer_widget'
            ),
            [Output({'type': "Gauge", 'index': ALL}, 'value'),
             Output({'type': "Gauge", 'index': ALL}, 'max')],
            [Input('telemetry_data', 'data')],
            [State({'type': "Gauge", 'index': ALL}, 'label'),
             State({'type': "Gauge", 'index': ALL}, 'max')]
        )

from dash import ClientsideFunction

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
            [Output({'type': "Thermometer", 'index': ALL}, 'value'),
             Output({'type': "Thermometer", 'index': ALL}, 'max')],
            [Input('telemetry_data', 'data')],
            [State({'type': "Thermometer", 'index': ALL}, 'label'),
             State({'type': "Thermometer", 'index': ALL}, 'max')]
        )

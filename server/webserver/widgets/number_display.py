from dash import ClientsideFunction

from .base_widget import *
import dash_daq as daq


class NumberDisplay(BaseWidget):
    widget_name = "Number Display"
    widget_type = "NumberDisplay"

    def __init__(self):
        super().__init__()

    def create_widget(self):
        return daq.LEDDisplay(
            id=self.widget_id,
            value=0,
            label='int data',
            color="#FF5E5E"
        )

    @staticmethod
    def create_callback(app):
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_number_display'
            ),
            Output({'type': "NumberDisplay", 'index': ALL}, 'value'),
            Input('telemetry_data', 'data'),
            State({'type': "NumberDisplay", 'index': ALL}, 'label'),
            State({'type': "NumberDisplay", 'index': ALL}, 'value')
        )

from dash import ClientsideFunction, MATCH

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
            label='No source',
            color="#FF5E5E"
        )

    def create_settings_menu(self):
        return self._source_settings_menu()

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

        # Data source changed
        @app.callback(
            Output({'type': NumberDisplay.widget_type, 'index': MATCH}, 'label'),
            Input({'type': 'value_dropdown', 'index': MATCH}, 'value')
        )
        def select_data_source(val):
            if val is None:
                return 'No source'
            return val
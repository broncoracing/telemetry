from dash import ClientsideFunction, MATCH

from .base_widget import *
import dash_daq as daq


class IndicatorLight(BaseWidget):
    widget_name = "Indicator Light"
    widget_type = "Indicator"

    def __init__(self):
        super().__init__()

    def create_widget(self):
        return daq.Indicator(
            id=self.widget_id,
            value=0,
            label='No source',
            labelPosition="bottom",
            color="#FF5E5E",
            size=25,
        )

    def create_settings_menu(self):
        return self._source_settings_menu()

    @staticmethod
    def create_callback(app):
        # Data update callback
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_indicator'
            ),
            Output({'type': "Indicator", 'index': ALL}, 'value'),
            Input('telemetry_data', 'data'),
            State({'type': "Indicator", 'index': ALL}, 'label'),
        )

        # Data source changed
        @app.callback(
            Output({'type': IndicatorLight.widget_type, 'index': MATCH}, 'label'),
            Input({'type': 'value_dropdown', 'index': MATCH}, 'value')
        )
        def select_data_source(val):
            if val is None:
                return 'No source'
            return val

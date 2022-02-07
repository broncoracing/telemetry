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

    @classmethod
    def create_callback(cls, app):
        # Data update callback
        app.clientside_callback(
            ClientsideFunction(
                namespace='clientside',
                function_name='update_indicator'
            ),
            Output({'type': "Indicator", 'index': MATCH}, 'value'),
            Input('telemetry_data', 'data'),
            State({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')
        )

        # Data source changed
        @app.callback(
            [Output({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data'),
             Output({'type': "Indicator", 'index': MATCH}, 'label')],
            Input({'type': 'value_dropdown', 'index': MATCH}, 'value'),
            State({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')
        )
        def select_data_source(val, data):
            if val is None:
                val = 'No source'

            data['value'] = val
            return [data, val]

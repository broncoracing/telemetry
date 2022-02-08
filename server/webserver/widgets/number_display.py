from dash import ClientsideFunction, MATCH

from .base_widget import *
import dash_daq as daq


class NumberDisplay(BaseWidget):
    widget_name = "Number Display"
    widget_type = "NumberDisplay"

    def __init__(self, saved_data=None):
        super().__init__(saved_data)

    def create_widget(self):
        return daq.LEDDisplay(
            id=self.widget_id,
            value=0,
            label='No source',
            color="#FF5E5E"
        )

    def create_settings_menu(self):
        return self._source_settings_menu()

    @classmethod
    def create_callback(cls, app):
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
            Output({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data'),
            Input({'type': 'value_dropdown', 'index': MATCH}, 'value'),
            State({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')
        )
        def select_data_source(val, data):
            if val is None:
                val = 'No source'
            data['value'] = val
            return data

        @app.callback(
            Output({'type': "NumberDisplay", 'index': MATCH}, 'label'),
            Input({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')
        )
        def set_label(data):
            if data is None:
                return 'No data'
            elif 'value' in data.keys():
                return data['value']
            else:
                return 'No data'

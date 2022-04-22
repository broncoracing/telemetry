from dash import ClientsideFunction, MATCH

from .base_widget import *
import dash_bootstrap_components as dbc


class ButtonPreset:
    def __init__(self, button_text, color, frame_id=999, data=b''):
        self.button_text = button_text
        self.color = color
        self.frame_id = frame_id
        self.data = data


BUTTON_PRESETS = {
    'Remote Start': ButtonPreset('Start Car', color="danger"),
    'Rainbow mode': ButtonPreset('Engage rainbow mode', color="info"),
    'Dim brake light': ButtonPreset('Dim brake light', color="dark"),
}


class Button(BaseWidget):
    widget_name = "Gauge"
    widget_type = "Gauge"

    def __init__(self, saved_data=None):
        super().__init__(saved_data)

    def create_widget(self):
        return dbc.Button(
            "(Choose a setting...)", color="primary", className="me-1",
            id=self.widget_id
        )

    def create_settings_menu(self):
        return [
            html.Div(
                [
                    'Button preset:',
                    dcc.Dropdown(
                        BUTTON_PRESETS.keys(),
                        id={'index': self.random_id, 'type': 'button_preset_dropdown'}
                    )
                ]
            )
        ]

    @classmethod
    def create_callback(cls, app):
        pass
        # app.clientside_callback(
        #     ClientsideFunction(
        #         namespace='clientside',
        #         function_name='update_thermometer_widget'
        #     ),
        #     [Output({'type': "Gauge", 'index': MATCH}, 'value'),
        #      Output({'type': "Gauge", 'index': MATCH}, 'max'),
        #      Output({'type': "Gauge", 'index': MATCH}, 'min'),
        #      Output({'type': "Gauge", 'index': MATCH}, 'label')
        #      ],
        #     [Input('telemetry_data', 'data'),
        #      Input({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')],
        # )
        #
        # # Data source changed
        # @app.callback(
        #     [Output({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data')],
        #     [Input({'type': 'value_dropdown', 'index': MATCH}, 'value'),
        #      Input({'type': 'gauge_min_value', 'index': MATCH}, 'value'),
        #      Input({'type': 'gauge_max_value', 'index': MATCH}, 'value')],
        #     [State({'type': cls.get_widget_data_type(), 'index': MATCH}, 'data'),
        #      State({'type': 'settings_btn', 'index': MATCH}, 'n_clicks')]
        # )
        # def update_settings(value, scale_min, scale_max, data, settings_clicks):
        #     if settings_clicks is None or settings_clicks == 0:
        #         raise PreventUpdate
        #     print(data)
        #
        #     if value is None:
        #         value = 'No source'
        #     if scale_min is None:
        #         scale_min = 0
        #     if scale_max is None:
        #         scale_max = 10
        #
        #     data['value'] = value
        #     data['min'] = scale_min
        #     data['max'] = scale_max
        #
        #     return [data]

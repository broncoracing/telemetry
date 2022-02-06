import dash

import dash_bootstrap_components as dbc
from dash import dcc, Dash
import dash_daq as daq
from dash import Input, Output, html, State, ALL
from dash.exceptions import PreventUpdate
import plotly.express as px

import uuid


class BaseWidget:
    widget_name = "Default name, please override"
    widget_type = "DefaultType"

    def __init__(self):
        # Generate a random ID for the widget, this is so that it can be uniquely identified even if there are multiple on the page.
        self.random_id = str(uuid.uuid4())
        # Create an ID which contains a type and index. The type is used so that a callback below can be applied to a type of widget
        # instead of each widget individually.
        self.widget_id = {'index': self.random_id, 'type': self.widget_type}
        # Create the widget and wrap it in a <span>. The id of the span is just the random uuid with no type.
        self.widget = html.Span([
            dbc.Row([
                dbc.Button(id={'index': self.random_id, 'type': 'close_btn'}, class_name='btn-close'),
                dbc.Button(id={'index': self.random_id, 'type': 'settings_btn'}, class_name='btn-close btn-settings')
            ], class_name='hover-row'),
            self.create_widget(),
            dbc.Offcanvas(
                self.create_settings_menu(),
                id={'index': self.random_id, 'type': 'settings_menu'},
                title=self.widget_name,
                is_open=False,
            ),
        ], id=self.random_id, className='widget-container')

    # Return the actual widget element. This will be wrapped in an html <span> to make adding/removing/moving easier.
    def create_widget(self):
        pass

    # Return the settings menu for modifying the widget. This is what will appear when the settings icon is clicked.
    def create_settings_menu(self):
        return "No settings available"

    # Settings menu for setting source
    def _source_settings_menu(self):
        return html.Div(
            [
                'Data source:',
                dcc.Dropdown(id={'index': self.random_id, 'type': 'value_dropdown'})
            ]
        )

    # Create necessary callbacks in the app. This is a static method because it only needs to be run once for all widgets of a given type.
    @staticmethod
    def create_callback(app: Dash):
        pass

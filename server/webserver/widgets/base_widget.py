import dash

import dash_bootstrap_components as dbc
from dash import dcc
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
        random_id = str(uuid.uuid4())
        # Create an ID which contains a type and index. The type is used so that a callback below can be applied to a type of widget
        # instead of each widget individually.
        self.widget_id = {'index': random_id, 'type': "Graph"}
        # Create the widget and wrap it in a <span>. The id of the span is just the random uuid with no type.
        self.widget = html.Span(self.create_widget(), id=random_id)

    # Return the actual widget element. This will be wrapped in an html <span> to make adding/removing/moving easier.
    def create_widget(self):
        pass

    # Create necessary callbacks in the app. This is a static method because it only needs to be run once for all widgets of a given type.
    @staticmethod
    def create_callback(app):
        pass

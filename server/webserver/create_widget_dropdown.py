import dash
from dash import Input, Output, html, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from .widgets import telemetry_widgets


ADD_DROPDOWN_TYPE = "add_dropdown"

dropdown = dbc.DropdownMenu(
    label="Add item",
    children=[
        dbc.DropdownMenuItem(widget.widget_name, id={'type': ADD_DROPDOWN_TYPE, 'index': widget.widget_type}, n_clicks=0) for widget in
        telemetry_widgets.values()
    ],
    direction="end"
)


# Create callbacks for the widget creation dropdown
def create_dropdown_callback(app):
    # This is called when a dropdown item is selected.
    @app.callback(
        Output("draggable", "children"),
        Input({'type': ADD_DROPDOWN_TYPE, 'index': ALL}, 'n_clicks'),
        State("draggable", "children"),
    )
    def add_element(n, children):
        if all(val == 0 for val in n):
            raise PreventUpdate

        ctx = dash.callback_context

        # handle mystery clicks (nothing was actually pressed
        if not ctx.triggered:
            raise PreventUpdate
        else:
            # Get the id of the clicked button. This is the type of the widget to create.
            button_id = ctx.triggered[0]['prop_id'].split('"')[3]

            # Create the widget and add it to the layout.
            new_item = telemetry_widgets[button_id]()
            children.append(new_item.widget)
            return children

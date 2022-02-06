import dash
from dash import Input, Output, html, State, ALL, MATCH
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
    # direction="end",
    nav=True,
    in_navbar=True,
)


# Create callbacks for the widget creation dropdown
def create_widget_management_callbacks(app):
    # This is called when a dropdown item is selected.
    @app.callback(
        Output("draggable", "children"),
        Input({'type': ADD_DROPDOWN_TYPE, 'index': ALL}, 'n_clicks'),
        Input({'type': 'close_btn', 'index': ALL}, 'n_clicks'),
        State("draggable", "children"),
    )
    def add_or_remove_widget(create, close, children):
        if all(val == 0 for val in create) and all(val == 0 for val in close):
            raise PreventUpdate

        ctx = dash.callback_context

        # handle mystery clicks (nothing was actually pressed
        if not ctx.triggered:
            raise PreventUpdate
        else:
            # Get the id of the clicked button. This is the type of the widget to create.
            button_id = ctx.triggered[0]['prop_id'].split('"')[3]
            # print(button_id)

            if button_id in telemetry_widgets.keys():
                # Create the widget and add it to the layout.
                new_item = telemetry_widgets[button_id]()
                children.append(new_item.widget)
            else:
                for child in children:
                    if child['props']['id'] == button_id:
                        children.remove(child)

            return children

    # callback to toggle the settings menu visibility
    @app.callback(
        Output({'type': 'settings_menu', 'index': MATCH}, "is_open"),
        Input({'type': 'settings_btn', 'index': MATCH}, 'n_clicks'),
        [State({'type': 'settings_menu', 'index': MATCH}, "is_open")],
    )
    def toggle_settings_menu(n1, is_open):
        if n1:
            return not is_open
        return is_open

    # Adds the current data options to all dropdown menus
    @app.callback(
        Output({'type': 'value_dropdown', 'index': MATCH}, 'options'),
        Input({'type': 'settings_btn', 'index': MATCH}, 'n_clicks'),
        State("telemetry_data_columns", "data")
    )
    def update_value_dropdown(_n, data):
        print(data)
        return [{"label": i, "value": i} for i in data]


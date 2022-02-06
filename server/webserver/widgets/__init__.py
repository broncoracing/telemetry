import dash
from dash import Input, ALL, MATCH, State, Output
from dash.exceptions import PreventUpdate

from .base_widget import BaseWidget

from pkgutil import iter_modules
from pathlib import Path
from importlib import import_module
from inspect import isclass

'''
The following code imports every available subclass of BaseWidget and adds it to telemetry_widgets.
This means that all that has to be done to create an additional widget is to create a subclass of BaseWidget in 
a file in this package.
'''


telemetry_widgets = {}

# iterate through the modules in the current package
package_dir = str(Path(__file__).resolve().parent)
for (_, module_name, _) in iter_modules([package_dir]):

    # import the module and iterate through its attributes
    module = import_module(f"{__name__}.{module_name}")
    for attribute_name in dir(module):
        attribute = getattr(module, attribute_name)

        # If the attribute is a subclass of BaseWidget, add it to the telemetry_widgets dictionary (But not if it is base_widget itself!)
        if isclass(attribute) and issubclass(attribute, BaseWidget) and attribute != BaseWidget:
            # Add the class to the widget dictionary
            telemetry_widgets[attribute.widget_type] = attribute


def create_widget_callbacks(app):
    for widget in telemetry_widgets.values():
        widget.create_callback(app)

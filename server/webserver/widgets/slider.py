from .base_widget import *


class Slider(BaseWidget):
    widget_name = "Slider"
    widget_type = "Slider"

    def __init__(self):
        super().__init__()

    def create_widget(self):
        return dcc.Slider(
            id=self.widget_id,
            min=0,
            max=4,
            value=0,
            marks={str(year): str(year) for year in range(5)},
            step=None
        )

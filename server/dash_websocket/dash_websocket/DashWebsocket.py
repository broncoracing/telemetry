# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashWebsocket(Component):
    """A DashWebsocket component.
DashWebsocket is an adapter for websocket.
It takes two property, `port` and 'msg'
`port` indicates the websocket url port
`msg` display the message returns from webscoket

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- msg (string; optional):
    The websocket response message.

- port (string; required):
    The port for websocket."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, msg=Component.UNDEFINED, port=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'msg', 'port']
        self._type = 'DashWebsocket'
        self._namespace = 'dash_websocket'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'msg', 'port']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['port']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashWebsocket, self).__init__(**args)

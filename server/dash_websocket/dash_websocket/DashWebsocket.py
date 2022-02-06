# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashWebsocket(Component):
    """A DashWebsocket component.
DashWebsocket is an adapter for websocket.
It takes two property, `url` and 'msg'
`url` indicates the websocket url
`msg` display the message returns from webscoket

Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- msg (string; optional):
    The websocket response message.

- url (string; required):
    The url for websocket."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, msg=Component.UNDEFINED, url=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'msg', 'url']
        self._type = 'DashWebsocket'
        self._namespace = 'dash_websocket'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'msg', 'url']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['url']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(DashWebsocket, self).__init__(**args)

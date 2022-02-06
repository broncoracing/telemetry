# AUTO GENERATED FILE - DO NOT EDIT

export dashwebsocket

"""
    dashwebsocket(;kwargs...)

A DashWebsocket component.
DashWebsocket is an adapter for websocket.
It takes two property, `url` and 'msg'
`url` indicates the websocket url
`msg` display the message returns from webscoket
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `msg` (String; optional): The websocket response message.
- `url` (String; required): The url for websocket.
"""
function dashwebsocket(; kwargs...)
        available_props = Symbol[:id, :msg, :url]
        wild_props = Symbol[]
        return Component("dashwebsocket", "DashWebsocket", "dash_websocket", available_props, wild_props; kwargs...)
end


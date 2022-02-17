# AUTO GENERATED FILE - DO NOT EDIT

export dashwebsocket

"""
    dashwebsocket(;kwargs...)

A DashWebsocket component.
DashWebsocket is an adapter for websocket.
It takes two property, `port` and 'msg'
`port` indicates the websocket url port
`msg` display the message returns from webscoket
Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `msg` (String; optional): The websocket response message.
- `port` (String; required): The port for websocket.
"""
function dashwebsocket(; kwargs...)
        available_props = Symbol[:id, :msg, :port]
        wild_props = Symbol[]
        return Component("dashwebsocket", "DashWebsocket", "dash_websocket", available_props, wild_props; kwargs...)
end


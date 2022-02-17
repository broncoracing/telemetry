# AUTO GENERATED FILE - DO NOT EDIT

dashWebsocket <- function(id=NULL, msg=NULL, port=NULL) {
    
    props <- list(id=id, msg=msg, port=port)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DashWebsocket',
        namespace = 'dash_websocket',
        propNames = c('id', 'msg', 'port'),
        package = 'dashWebsocket'
        )

    structure(component, class = c('dash_component', 'list'))
}

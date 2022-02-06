# AUTO GENERATED FILE - DO NOT EDIT

#' @export
dashWebsocket <- function(id=NULL, msg=NULL, url=NULL) {
    
    props <- list(id=id, msg=msg, url=url)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'DashWebsocket',
        namespace = 'dash_websocket',
        propNames = c('id', 'msg', 'url'),
        package = 'dashWebsocket'
        )

    structure(component, class = c('dash_component', 'list'))
}

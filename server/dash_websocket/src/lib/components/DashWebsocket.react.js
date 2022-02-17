import React, {Component} from 'react';
import PropTypes from 'prop-types';
import { w3cwebsocket as W3CWebSocket } from "websocket";

/**
 * DashWebsocket is an adapter for websocket.
 * It takes two property, `port` and 'msg'
 * `port` indicates the websocket url port
 * `msg` display the message returns from webscoket
 */
export default class DashWebsocket extends Component {
    componentDidMount() {
        const doc_url = new URL(document.URL)
        const url = "ws://" + doc_url.hostname + ':' + this.props.port;
        console.log('Websocket client connecting to ' + url);
        const client = new W3CWebSocket(url);
        client.onopen = () => {
            console.log('websocket connected');
        }
        client.onmessage = (message) => {
            this.props.setProps({ msg: message.data})
        }
    }


    render() {
        return null; // Invisible
    }
}

DashWebsocket.defaultProps = {};

DashWebsocket.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * The websocket response message.
     */
    msg: PropTypes.string,

    /**
     * The port for websocket.
     */
    port: PropTypes.string.isRequired,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func
};
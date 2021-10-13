import {Sock} from "../models/sock.model";

// builds the WS and write to the store the new value received
let _build_websocket = (url: string, channel: string): Sock => {
    let socket = new Sock(url, channel);

    return socket;
};

let _websockets = {}

export let get_websocket = (url: string, channel: string): Sock => {
    if (!_websockets[url + channel] || _websockets[url + channel].isdead) {
        _websockets[url + channel] = _build_websocket(url, channel);
    }
    return _websockets[url + channel];
}

export let close_websocket = (url, channel) => {
    if (_websockets[url + channel] !== undefined) {
        delete _websockets[url + channel];
    }
}
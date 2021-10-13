import {Sock} from "../models/sock.model";

// builds the WS and write to the store the new value received
let _build_websocket = (channel: string): Sock => {
    let socket = new Sock(channel);

    return socket;
};

let _websockets = {}

export let get_websocket = (channel: string): Sock => {
    if (!_websockets[channel] || _websockets[channel].isdead) {
        _websockets[channel] = _build_websocket(channel);
    }
    return _websockets[channel];
}

export let close_websocket = (channel) => {
    if (_websockets[channel] !== undefined) {
        delete _websockets[channel];
    }
}
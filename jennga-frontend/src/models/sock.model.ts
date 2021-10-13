export class Sock {
    private socket: WebSocket;
    public callbacks: ((object) => void)[] = [];
    public isdead = false;

    constructor(url: string, channel: string) {
        this.socket = new WebSocket(url + "/" + channel);
        console.log(`Connecting to ${url}/${channel}`);

        this.socket.onopen = function (e) {
            console.log(`[open] Connection established to chanel ${channel}`);
        };

        let ctx = this;
        this.socket.onmessage = function (event) {
            try {
                const data = JSON.parse(event.data);
                console.log(`[message] Data received from server (json): ${event.data}`);
                ctx.callbacks.forEach(element => {
                    element(data);
                });
            } catch {
                console.error(`[message] Data received from server (NOT json): ${event.data}`);
            }
        };

        this.socket.onclose = function (event) {
            if (event.wasClean) {
                console.log(
                    `[close] Connection closed cleanly, code=${event.code} reason=${event.reason}`
                );
            } else {
                // e.g. server process killed or network down
                // event.code is usually 1006 in this case
                console.warn("[close] Connection died");
            }
            ctx.isdead = true;
        };

        this.socket.onerror = function (error) {
            console.warn(`[error] ${error}`);
        };
    }

    public send(data: object): void {
        console.log(`Sending ${JSON.stringify(data)}`);
        
        this.socket.send(JSON.stringify(data));
    }
}
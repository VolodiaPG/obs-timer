import { init } from "svelte/internal";

export class Sock {
    private socket: WebSocket;
    public callbacks: ((object) => void)[] = [];
    public isdead = false;

    constructor(private url: string, private channel: string) {
        this.init()
    }

    private init(): void {
        this.socket = new WebSocket(this.url + "/" + this.channel);
        console.log(`Connecting to ${this.url}/${this.channel}`);

        this.socket.onopen = function (e) {
            console.log(`[open] Connection established to chanel ${this.channel}`);
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
            setTimeout(function() {
                ctx.init();
              }, 1000);
        };

        this.socket.onerror = function (error) {
            console.warn(`[error] ${error}`);
            ctx.socket.close();
        };
    }

    public send(data: object): void {
        console.log(`Sending ${JSON.stringify(data)}`);
        
        this.socket.send(JSON.stringify(data));
    }
}
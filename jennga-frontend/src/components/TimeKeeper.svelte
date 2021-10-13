<script lang="ts">
    import { Timer } from "../models/Timer.model";

    import { get_websocket } from "../stores/websocket.store";
    const URL = "ws://localhost:8000/ws";
    let timer = new Timer();
    export let player: string;

    let socket = get_websocket(URL, "timer");
    socket.callbacks.push((data) => {
       timer = Object.assign(timer, data)
    });

    
</script>

<main>
    <span>{timer[player]}</span>
</main>
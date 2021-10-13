<script lang="ts">
    import { Timer } from "../models/Timer.model";
    import { get_websocket } from "../stores/websocket.store";
    
    let timer = new Timer();
    export let player: string;

    let socket = get_websocket("timer");
    socket.callbacks.push((data) => {
       timer = Object.assign(timer, data)
    });

    
</script>

<main>
    <span>{timer[player]}</span>
</main>
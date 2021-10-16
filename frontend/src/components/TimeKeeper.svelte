<script lang="ts">
    import { Timer } from "../models/Timer.model";
    import { get_websocket } from "../stores/websocket.store";

    let timer = new Timer();
    export let player: string;
    let timer_active = false;

    let socket = get_websocket("timer");
    socket.callbacks.push((data) => {
        timer = Object.assign(timer, data);
        timer_active = data.active[player];
    });
</script>

<main>
    <span class={timer_active ? "active" : "inactive"}>{timer[player]}</span>
</main>

<style>
    .inactive {
        font-style: normal;
    }
    .active {
        font-style: italic;
    }
</style>

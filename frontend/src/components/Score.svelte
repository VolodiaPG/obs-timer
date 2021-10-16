<script lang="ts">
    import { get_websocket } from "../stores/websocket.store";
    
    export let player: string;
    let score: number = 0;

    let socket = get_websocket("scores");
    socket.callbacks.push((data) => {
        score = data[player];
    });

    let timer_active = false;

    let socket_timer = get_websocket("timer");
    socket_timer.callbacks.push((data) => {
        timer_active = data.active[player];
    });
</script>

<main>
    <span class={timer_active ? "active" : "inactive"}>{score}</span>
</main>

<style>
    .inactive{
        font-style: normal;
    }
    .active{
        font-style: italic;
    }
</style>

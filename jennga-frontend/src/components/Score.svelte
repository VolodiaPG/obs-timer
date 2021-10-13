<script lang="ts">
    import { get_websocket } from "../stores/websocket.store";
    const URL = "ws://localhost:8000/ws";
    export let player: string;
    let score: number = 0;

    let socket = get_websocket(URL, "scores");
    socket.callbacks.push((data) => {
        score = data[player];
    });
</script>

<main>
    <span>{score}</span>
</main>

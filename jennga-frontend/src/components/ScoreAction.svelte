<script lang="ts">
    import { get_websocket } from "../stores/websocket.store";
    const URL = "ws://localhost:8000/ws";
    export let player: string;
    let increment: number = 1;

    let socket = get_websocket(URL, "scores");

    let send = () => {
        socket.send({
            [player]: increment
        });
    }
</script>

<main>
    <input bind:value={increment} />
    <button on:click={send}>Increment</button>
</main>

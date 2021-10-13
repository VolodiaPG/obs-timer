<script lang="ts">
    import { get_websocket } from "../stores/websocket.store";
    export let player: string;
    let increment: number = 1;

    let socket = get_websocket("scores");

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

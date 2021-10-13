<script lang="ts">
    import { onMount } from "svelte";

    import { get_websocket } from "../stores/websocket.store";
    const URL = "ws://localhost:8000/ws";
    const FETCH_URL = "http://localhost:8000/scores";
    export let player: string;
    let score: number = 0;

    onMount(async () => {
        fetch(FETCH_URL)
            .then((response) => response.json())
            .then((data) => {
                score = data[player];
            })
            .catch((error) => {
                console.log(error);
            });
    });

    let socket = get_websocket(URL, "scores");
    socket.callbacks.push((data) => {
        score = data[player];
    });
</script>

<main>
    <span>{score}</span>
</main>

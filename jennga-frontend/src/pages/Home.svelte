<script lang="ts">
    import Score from "../components/Score.svelte";
    import ScoreAction from "../components/ScoreAction.svelte";
    import TimeKeeper from "../components/TimeKeeper.svelte";
    import { Action, ActionTypes } from "../models/Action.model";

    import { get_websocket } from "../stores/websocket.store";
    const URL = "ws://localhost:8000/ws";
    const RESET_URL = "http://localhost:8000/reset";
    let messages = [];
    let message: string;

    var socket_gen = get_websocket(URL, "test");
    socket_gen.callbacks.push((data) => {
        messages = [...messages, data["message"]];
    });
    var socket_action = get_websocket(URL, "actions");

    function send_gen(message: string) {
        socket_gen.send({ message: message });
        message = "";
    }

    function send_action(action_type: ActionTypes) {
        let action = new Action(action_type);
        console.log(action);

        socket_action.send(action);
    }

    function reset() {
        fetch(RESET_URL, { method: "POST" });
    }
</script>

<main>
    <div>Player 1</div>
    <TimeKeeper player="p1" />
    <Score player="p1" />
    <ScoreAction player="p1" />
    <div>Player 2</div>
    <TimeKeeper player="p2" />
    <Score player="p2" />
    <ScoreAction player="p2" />
    <input bind:value={message} />
    <button on:click={() => send_gen(message)}>Send</button>
    <button on:click={() => send_action(ActionTypes.PAUSE)}>Pause</button>
    <button on:click={() => send_action(ActionTypes.NEXT)}>Next</button>
    <button on:click={() => send_action(ActionTypes.RESET)}>Reset</button>
    <button on:click={reset}>Reset All</button>
    <ul>
        {#each messages as msg}
            <li>{msg}</li>
        {/each}
    </ul>
</main>

<style>
    main {
        text-align: center;
        padding: 1em;
        max-width: 240px;
        margin: 0 auto;
    }

    h1 {
        color: #ff3e00;
        text-transform: uppercase;
        font-size: 4em;
        font-weight: 100;
    }

    @media (min-width: 640px) {
        main {
            max-width: none;
        }
    }
</style>

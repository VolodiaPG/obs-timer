<script lang="ts">
    import PlayerBackground from "../components/PlayerBackground.svelte";
    import PlayerControl from "../components/PlayerControl.svelte";
    import Score from "../components/Score.svelte";
    import ScoreAction from "../components/ScoreAction.svelte";
    import TimeKeeper from "../components/TimeKeeper.svelte";
    import { Action, ActionTypes } from "../models/Action.model";

    import { get_websocket } from "../stores/websocket.store";
    const URL = "ws://localhost:8000/ws";
    const RESET_URL = "http://localhost:8000/reset";

    let time = 30;
    let fischer = 5;

    let socket_action = get_websocket(URL, "actions");
    let socket_clock = get_websocket(URL, "clock");

    function send_action(action_type: ActionTypes) {
        let action = new Action(action_type);
        socket_action.send(action);
    }

    function reset() {
        fetch(RESET_URL, { method: "POST" });
    }

    socket_clock.callbacks.push((clock) => {
        time = clock.counter;
        fischer = clock.fischer;
    });
    async function new_clock() {
        socket_clock.send({ counter: time, fischer: fischer });
    }
</script>

<main>
    {#each ["p1", "p2"] as player}
        <div class="wrapper">
            <PlayerControl {player} />
        </div>
    {/each}
    <div class="wrapper">
        <button on:click={() => send_action(ActionTypes.PAUSE)}>Pause</button>
        <button on:click={() => send_action(ActionTypes.NEXT)}>Next</button>
        <button on:click={() => send_action(ActionTypes.RESET)}>Reset</button>
        <button on:click={reset}>Reset All</button>
        <form on:submit|preventDefault={new_clock}>
            <input placeholder="Time" bind:value={time} />
            <input placeholder="Fischer" bind:value={fischer} />
            <button type="submit">Apply</button>
        </form>
    </div>
</main>

<style>
    main {
        text-align: center;
        /* padding: 1em; */
        /* margin: 0 auto; */
        width: 100%;
        height: 100%;
    }

    /*Material card*/
    .wrapper {
        padding: 10px;
        position: relative;
        width: 90%;
        height: 100%;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        border-radius: 10px;
        margin: 10px auto;
    }
</style>

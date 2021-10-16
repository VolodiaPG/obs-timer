<script lang="ts">
    import PlayerBackground from "../components/PlayerBackground.svelte";
    import Score from "../components/Score.svelte";
    import TimeKeeper from "../components/TimeKeeper.svelte";
    import ToggleFullscreen from "../components/ToggleFullscreen.svelte";
    import { Action, ActionTypes } from "../models/Action.model";
    import { get_websocket } from "../stores/websocket.store";

    export let player = "p1";

    let socket_action = get_websocket("actions");
    let timer_active = false;

    let invert_player = () => {
        return player === "p1" ? "p2" : "p1";
    };

    function send_action(action_type: ActionTypes) {
        let action = new Action(action_type);
        socket_action.send(action);
    }

    let socket_timer = get_websocket("timer");
    socket_timer.callbacks.push((data) => {
        timer_active = data.active[player];
    });
</script>

<main>
    <div class="options">
        <span class="left">{player == "p1" ? "Player #1" : "Player #2"}</span>
        <span class="in-line">
            <div>
                <button on:click={() => send_action(ActionTypes.PAUSE)}
                    >Pause</button
                >
            </div>
            <div>
                <ToggleFullscreen />
            </div>
        </span>
        <span class="right">
            <span class="myscore">
                <Score {player} />
            </span>
            vs.
            <span>
                <Score player={invert_player()} />
            </span>
        </span>
    </div>
    <PlayerBackground {player} {timer_active} />
    <div class="take-all-view">
        <button
            class="next-button"
            disabled={!timer_active}
            on:click={() => send_action(ActionTypes.NEXT)}
        >
            <span class="timer">
                <TimeKeeper {player} />
            </span>
        </button>
    </div>
</main>

<style>
    main {
        text-align: center;
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
    }

    .take-all-view{
        height: 100%;
        width: 100%;
    }

    .next-button {
        width: 100%;
        height: 100%;
        background-color: transparent;
        border: 0;
        margin: 0;
        padding: 0;
    }

    .left,
    .right {
        margin-left: 5px;
        margin-right: 5px;
    }

    .left {
        position: absolute;
        left: 0;
    }

    .right {
        position: absolute;
        right: 0;
    }

    /*make the timer big and white*/
    .timer {
        font-size: 5em;
        color: white;
        transition: 1000ms linear;
    }

    /*Hightlight  my score with a red background and a radius of 2px and add spacing*/
    .myscore {
        background-color: red;
        border-radius: 2px;
        padding: 0.2em;
        color: white;
    }

    /*Make a centered bottom bar and align vertically*/
    .options {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        padding: 2px 0;
        height: min-content;
        background-color: #f0f0f0;
        z-index: 3;
    }

    /*Make the content be on one line*/
    .options > * > * {
        display: inline-block;
        vertical-align: middle;
    }

    /*Set the content of the in-line class to be on the same line */
    .in-line {
        display: flex;
        align-items: center;
    }
    .in-line > div {
        margin-left: 5px;
        margin-right: 5px;
    }
    button{
        margin:0
    }
</style>

<script lang="ts">
    import PlayerBackground from "../components/PlayerBackground.svelte";
    import Score from "../components/Score.svelte";
    import TimeKeeper from "../components/TimeKeeper.svelte";
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
        <button on:click={() => send_action(ActionTypes.PAUSE)}>Pause</button>
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
    <div>
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
    }

    .background {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
    }

    .next-button {
        width: 100vw;
        height: 100vh;
        background-color: transparent;
        border: 0;
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
        padding: 2px;
        height: min-content;
        background-color: #f0f0f0;
        z-index: 3;
    }

    /*Make the content be on one line*/
    .options > * > * {
        display: inline-block;
        vertical-align: middle;
    }

    @keyframes gradient {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    .inactive {
        background: linear-gradient(-45deg, #000, #ccc);
    }
    .p1 {
        background: linear-gradient(-45deg, #61045f, #aa076b);
    }
    .p2 {
        background: linear-gradient(-45deg, #f5af19, #f12711);
    }
    .p1,
    .p2,
    .inactive {
        width: 100vw;
        height: 100vh;
        background-size: 400% 400%;
    }
    .p1,
    .p2 {
        animation: gradient 5s cubic-bezier(0.25, 0.46, 0.45, 0.94) infinite;
    }

    .fade-in {
        animation: fade-in 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
    }

    .fade-out {
        animation: fade-out 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
        opacity: 0;
    }

    @keyframes fade-in {
        0% {
            opacity: 0;
        }
        100% {
            opacity: 1;
        }
    }
    @keyframes fade-out {
        0% {
            opacity: 1;
        }
        100% {
            opacity: 0;
        }
    }
</style>

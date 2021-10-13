<script lang="ts">
    import PlayerBackground from "../components/PlayerBackground.svelte";
    import Score from "../components/Score.svelte";
    import ScoreAction from "../components/ScoreAction.svelte";
    import TimeKeeper from "../components/TimeKeeper.svelte";

    import { get_websocket } from "../stores/websocket.store";

    export let player = "p1";

    let timer_active = false;

    let socket_timer = get_websocket("timer");
    socket_timer.callbacks.push((data) => {
        timer_active = data.active[player];
    });
</script>

<main>
    <PlayerBackground {player} {timer_active} />
    <h3>{player}</h3>
    <h1>
        <TimeKeeper {player} />
    </h1>
    <h2>
        <Score {player} />
    </h2>
    <ScoreAction {player} />
</main>

<style>
    main {
        border-radius: inherit;
    }

    h1,
    h2,
    h3 {
        color: white;
    }
</style>

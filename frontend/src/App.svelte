<script lang="ts">
    import { Router, Route } from "svelte-routing";
    import Home from "./pages/Home.svelte";
    import Player from "./pages/Player.svelte";
    import Scorer from "./pages/Scorer.svelte";
    import Timer from "./pages/Timer.svelte";
    export let url = ""; //This property is necessary declare to avoid ignore the Router
</script>

<main>
    <Router {url}>
        <Route path="timer/:player" let:params>
            <Timer player={params.player} />
        </Route>
        <Route path="score/:player" let:params>
            <Scorer player={params.player} />
        </Route>
        <Route path="player/:player" let:params>
            <Player player={params.player} />
        </Route>
        <Route path="/"><Home /></Route>
    </Router>
</main>

<style>
    main{
        width: 100%;
        height: 100%;
    }
</style>

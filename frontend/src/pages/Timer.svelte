<script lang="ts">
    import TimeKeeper from "../components/TimeKeeper.svelte";
    export let player: string;
</script>

<main>
    <span><TimeKeeper {player} /></span>
</main>

<style>
    span {
        font-size: 5em;
    }
</style>

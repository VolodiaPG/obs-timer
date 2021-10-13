<script lang="ts">
    import TimeKeeper from "../components/TimeKeeper.svelte";
    export let player:string;
</script>

<main>
    <span>{player}:<TimeKeeper player="{player}" /></span>
</main>

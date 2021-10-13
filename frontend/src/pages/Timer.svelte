<script lang="ts">
    import TimeKeeper from "../components/TimeKeeper.svelte";
    export let player:string;
</script>

<main>
    <span><TimeKeeper player="{player}" /></span>
</main>

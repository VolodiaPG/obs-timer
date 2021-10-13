<script lang="ts">
    import Score from "../components/Score.svelte";

    export let player: string;
</script>

<main>
    <span><Score {player} /></span>
</main>

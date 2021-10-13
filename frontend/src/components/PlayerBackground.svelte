<script lang="ts">
    export let player = "p1";

    export let timer_active = false;
</script>

<main>
    <div class="background inactive">
        <div class={timer_active ? "fade-in" : "fade-out"}>
            <div class:p1={player == "p1"} class:p2={player == "p2"} />
        </div>
    </div>
</main>

<style>
    main {
        margin: 0;
        padding: 0;
        border: inherit;
        border-radius: inherit;
    }
    div {
        border: inherit;
        border-radius: inherit;
    }

    .background {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
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
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        height: 100%;
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

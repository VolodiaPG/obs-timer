<script lang="ts">
    import { Router, Route, Link } from "svelte-routing";
    import Home from "./pages/Home.svelte";
    import Timer from "./pages/Timer.svelte";
    export let url = ""; //This property is necessary declare to avoid ignore the Router
</script>

<main>
    <Router {url}>
        <!-- <nav>
           <Link to="/">Home</Link>
           <Link to="about">About</Link>
         </nav>
         <div> -->
        <Route path="timer/:player" let:params>
            <Timer player="{params.player}" />
        </Route>
        <!--for now the router just support case sensitive,
               one workaround colud be add two time the route
               Example.
              <Route path="About" component="{About}" /> 
           -->
        <Route path="/"><Home /></Route>
        <!-- </div> -->
    </Router>
</main>

<style></style>
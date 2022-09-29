<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/tracks">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>
  <RouterView />
</template>

<style scoped>
div#app {
  display: flex;
}

header {
  line-height: 1.5;
  max-height: 100vh;
  padding-right: calc(var(--section-gap) / 2);
}

header .wrapper {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
}

nav {
  width: 100%;

  text-align: left;
  margin-left: -1rem;
  font-size: 1rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
}
</style>

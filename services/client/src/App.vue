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
      <div class="site-name"><h1>Spotify Playlist Lookup</h1></div>
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
}

header .wrapper {
  display: flex;
  flex-direction: column;
}

nav {
  width: 100%;

  text-align: left;
  font-size: 1rem;
  font-weight: 600;
  border-bottom: 1px solid rgb(239, 239, 239);
}

nav a.router-link-exact-active {
  display: none;
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0.4rem 1rem;
}

nav a:first-of-type {
  border: 0;
}

div.site-name {
  width: 100%;
  display: block;
  margin: 3rem 0;
}

div.site-name h1 {
  text-align: center;
  font-size: 1.8rem;
  line-height: 2rem;
  font-weight: 700;
}
</style>

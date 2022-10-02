<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import FooterNotice from "./components/FooterNotice.vue";
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
  <FooterNotice />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

header .wrapper {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

nav {
  width: 100%;

  text-align: left;
  font-size: 1rem;
  font-weight: 600;
  border-bottom: 1px solid var(--color-border);
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
  margin-top: 0.5rem;
  margin-bottom: 2rem;
}

div.site-name h1 {
  text-align: center;
  font-size: 1.2rem;
  line-height: 2rem;
  font-weight: 700;
  color: gray;
}
</style>

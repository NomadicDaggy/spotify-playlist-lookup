<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import FooterNotice from "./components/FooterNotice.vue";
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <div class="left-links">
          <RouterLink to="/tracks">Home</RouterLink>
          <RouterLink to="/about">About</RouterLink>
        </div>
        <div class="right-links">
          <a href="https://buymeacoffee.com/nomadicdaggy" target="_blank">
            <div>
              <img
                id="bmc-logo"
                :src="'/bmc-logo.png'"
                alt="Buy Me a Coffee Logo"
              />
            </div>
          </a>
          <a
            href="https://github.com/NomadicDaggy/spotify-playlist-lookup"
            target="_blank"
          >
            <div>
              <img
                id="gh-logo"
                :src="'/GitHub-Mark-32px.png'"
                alt="Github Logo"
              />
            </div>
          </a>
        </div>
      </nav>
      <div class="site-name"><h1>Spotify Playlist Lookup</h1></div>
    </div>
  </header>
  <RouterView />
  <FooterNotice />
</template>

<style>
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

  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav div.left-links a.router-link-active {
  display: none;
}

nav div.left-links a {
  display: inline-block;
  padding: 0.4rem 1rem;
}

nav div.right-links {
  display: flex;
  flex-direction: row;
  padding-right: 1rem;
  gap: 1rem;
  align-items: center;
  padding-top: 5px;
}

nav div.right-links > a:hover {
  background-color: unset;
}

div.right-links img {
  width: 25px;
  height: 25px;
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
  color: var(--color-text);
}

@media only screen and (min-width: 768px) {
  div.site-name {
    position: relative;
    margin: 0 auto;
    width: fit-content;
    margin-top: -2.2rem;
  }

  header {
    margin-bottom: 2rem;
  }
}
</style>

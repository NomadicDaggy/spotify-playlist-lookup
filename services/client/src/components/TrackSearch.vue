<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

const searchTerm = ref("");
const statusText = ref("Enter text to search playlists by tracks they contain");

const fetchTracks = () => {
  axios
    .get("http://localhost:1337/api/v1/tracks?name=" + searchTerm.value)
    .then((response) => {
      console.log(response.data);
      let foundTrackCount = response.data["count"];
      statusText.value = `Found ${foundTrackCount} tracks.`;
    })
    .catch((error) => {
      console.log(error);
    });
};

function getTracks() {
  console.log(searchTerm.value);
  fetchTracks();
}
</script>

<template>
  <div class="track-search-container">
    <input v-model="searchTerm" @keyup.enter="getTracks" />
    <span>{{ statusText }}</span>
  </div>
</template>

<style>
input {
  min-width: 250px;
  margin: 20px auto;
  display: block;
}
</style>

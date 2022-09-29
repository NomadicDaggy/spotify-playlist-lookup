<script setup lang="ts">
import { ref } from "vue";
import type { Ref } from "vue";
import axios from "axios";

const searchTerm = ref("");
const statusText = ref("Enter text to search playlists by tracks they contain");
const tracks = ref();

const fetchTracks = () => {
  axios
    .get("http://localhost:1337/api/v1/tracks?name=" + searchTerm.value)
    .then((response) => {
      let foundTrackCount = response.data["count"];
      statusText.value = `Found ${foundTrackCount} tracks.`;

      tracks.value = response.data["tracks"];
    })
    .catch((error) => {
      console.log(error);
    });
};

function selectTrack(track: Ref) {
  console.log(track);
}
</script>

<template>
  <div class="track-search-container">
    <input v-model="searchTerm" @keyup.enter="fetchTracks" />
    <span>{{ statusText }}</span>
    <div id="tracks-container">
      <div
        v-for="track in tracks"
        :key="track.spotify_id"
        @click="selectTrack(track)"
      >
        {{ track.name }}
      </div>
    </div>
  </div>
</template>

<style>
input {
  min-width: 250px;
  margin: 20px auto;
  display: block;
}
</style>

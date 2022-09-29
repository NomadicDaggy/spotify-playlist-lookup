<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import TrackResult from "./TrackResult.vue";

const router = useRouter();
const route = useRoute();

const searchTerm = ref(route.query.name);
const statusText = ref("Enter text to search playlists by tracks they contain");
const tracks = ref();

const fetchTracks = () => {
  // add param to url
  router.replace({ name: "tracks", query: { name: searchTerm.value } });

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

if (searchTerm.value) {
  fetchTracks();
}
</script>

<template>
  <div class="track-search-container">
    <input v-model="searchTerm" @keyup.enter="fetchTracks" />
    <span>{{ statusText }}</span>
    <div class="tracks-container">
      <TrackResult
        v-for="(track, index) in tracks"
        :track="track"
        :index="index"
        :key="track.spotify_id"
      />
    </div>
  </div>
</template>

<style>
input {
  min-width: 250px;
  margin: 20px auto;
  display: block;
}

div.tracks-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>

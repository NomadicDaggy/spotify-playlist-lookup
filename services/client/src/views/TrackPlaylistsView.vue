<script setup lang="ts">
import { ref } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import PlaylistCard from "../components/PlaylistCard.vue";
import { useTrackStore } from "../stores/track";
import { storeToRefs } from "pinia";
import TrackCard from "../components/TrackCard.vue";

const route = useRoute();

const store = useTrackStore();
const { storedTrack } = storeToRefs(store);

const playlists = ref();
const getPlaylists = () => {
  axios
    .get(
      "http://localhost:1337/api/v1/tracks/" +
        storedTrack.value?.spotify_id +
        "/playlists"
    )
    .then((response) => {
      playlists.value = response.data["playlists"];
    })
    .catch((error) => {
      console.log(error);
    });
};

if (storedTrack.value) {
  getPlaylists();
} else {
  // If no value in pinia store, then the user has come here without first selecting a track,
  // rather they just followed a link straight to this page.
  // So we need to get the track from the url parameter from our backend api
  axios
    .get(
      "http://localhost:1337/api/v1/tracks?spotify_id=" +
        route.params.trackSpotifyID
    )
    .then((response) => {
      store.$patch({
        storedTrack: response.data,
      });
      console.log(response.data);
      getPlaylists();
    })
    .catch((error) => {
      console.log(error);
    });
}
</script>

<template>
  <div class="playlist-results-container">
    <!-- <span>{{ statusText }}</span> -->
    <TrackCard v-if="storedTrack" :track="storedTrack" :selected="true" />
    <div v-else>Loading...</div>

    <div class="playlists-container" v-if="playlists">
      <span class="status-text">Playlists containing selected track</span>
      <PlaylistCard
        v-for="(playlist, index) in playlists"
        :playlist="playlist"
        :index="index"
        :key="playlist.spotify_id"
      />
    </div>
    <div v-else>Loading...</div>
  </div>
</template>

<style>
div.playlist-results-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>

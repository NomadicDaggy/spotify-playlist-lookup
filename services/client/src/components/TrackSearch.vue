<script setup lang="ts">
import { ref } from "vue";
import type { Ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import TrackCard from "./TrackCard.vue";
import type Track from "./TrackCard.vue";
import { useTrackStore } from "../stores/track";
import { storeToRefs } from "pinia";

const router = useRouter();
const route = useRoute();

const store = useTrackStore();
// const { storedTrack } = storeToRefs(store);

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

const selectTrack = (track: Ref<typeof Track>) => {
  // TODO: pass track to pinia
  store.$patch({
    storedTrack: track,
  });

  router.push({
    name: "trackPlaylists",
    params: { trackSpotifyID: track.spotify_id },
  });
};
</script>

<template>
  <div class="track-search-container">
    <input v-model="searchTerm" @keyup.enter="fetchTracks" />
    <span>{{ statusText }}</span>
    <div class="tracks-container">
      <TrackCard
        v-for="(track, index) in tracks"
        :track="track"
        :selected="false"
        :index="index"
        :key="track.spotify_id"
        @click="selectTrack(track)"
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

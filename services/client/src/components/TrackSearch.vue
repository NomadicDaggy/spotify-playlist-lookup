<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import TrackCard from "./TrackCard.vue";
import type Track from "./TrackCard.vue";
import { useTrackStore } from "../stores/track";

const router = useRouter();
const route = useRoute();

const store = useTrackStore();
// const { storedTrack } = storeToRefs(store);

const searchTerm = ref(route.query.name);
const statusText = ref("Find playlists that contain a specific track");
const tracks = ref<typeof Track | null>(null);

const fetchTracks = () => {
  if (!searchTerm.value) {
    statusText.value =
      "Please enter text to search tracks by. It can even be just part of the track name.";

    return;
  }

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

const selectTrack = (track: any) => {
  store.$patch({
    storedTrack: track,
  });

  router.push({
    name: "trackPlaylists",
    params: {
      trackSpotifyID: track.spotify_id,
    },
  });
};
</script>

<template>
  <div class="track-search-container">
    <input
      v-model="searchTerm"
      @keyup.enter="fetchTracks"
      placeholder="Track name"
      class="track-name-input"
    />
    <span class="status-text">{{ statusText }}</span>
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
input.track-name-input {
  max-width: 80vw;
  height: 2rem;
  border: 1px solid black;
  border-radius: 14px;
  padding-left: 14px;
  margin: 0 auto;
  display: block;
  font-size: 1.2rem;
}

div.tracks-container {
  display: flex;
  flex-direction: column;
}

span.status-text {
  text-align: center;
  display: block;
  padding: 1rem;
}

@media only screen and (min-width: 768px) {
  div.tracks-container {
    max-width: 600px;
    margin: 0 auto;
  }
}
</style>

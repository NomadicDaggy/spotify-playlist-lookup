<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import PlaylistCard from "../components/PlaylistCard.vue";
import Track from "../components/TrackCard.vue";
import { useTrackStore } from "../stores/track";
import { storeToRefs } from "pinia";
import TrackCard from "../components/TrackCard.vue";

const router = useRouter();
const route = useRoute();

const store = useTrackStore();
const { storedTrack } = storeToRefs(store);

const playlists = ref();

// If no value in pinia store, then the user has come here without first selecting a track,
// rather they just followed a link straight to this page.
// So we need to get the track from the url parameter from our backend api
if (!storedTrack.value) {
  // TODO: ^
}
</script>

<template>
  <div class="playlist-results-container">
    <!-- <span>{{ statusText }}</span> -->
    <TrackCard :track="storedTrack" />
    <div class="playlists-container">
      <PlaylistCard
        v-for="(playlist, index) in playlists"
        :playlist="playlist"
        :index="index"
        :key="playlist.spotify_id"
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

div.playlist-results-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>

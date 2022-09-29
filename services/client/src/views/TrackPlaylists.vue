<script setup lang="ts">
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import PlaylistCard from "../components/PlaylistCard.vue";
import Track from "../components/TrackCard.vue";

const router = useRouter();
const route = useRoute();

const playlists = ref();

// TODO: get active track from pinia
const props = defineProps({
  track: Track,
});

props.track; // Track | undefined
console.log(props.track);
</script>

<template>
  <div class="playlist-results-container">
    <!-- <span>{{ statusText }}</span> -->
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

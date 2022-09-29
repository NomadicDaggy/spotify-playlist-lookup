<script setup lang="ts">
import {} from "vue";

export interface Playlist {
  name: {
    type: String;
    default: "";
    required: true;
  };
  spotify_id: {
    type: String;
    default: "";
    required: true;
  };
  image_url: {
    type: String;
    default: "";
    required: true;
  };
  owner_name: {
    type: String;
    default: "";
    required: true;
  };
  description: {
    type: String;
    default: "";
    required: true;
  };
}

export interface Props {
  playlist: Playlist;
}

const props = withDefaults(defineProps<Props>(), {});

props.playlist; // Playlist | undefined
</script>

<template>
  <div class="playlist-result-card">{{ playlist.name }}</div>
</template>

<style>
.playlist-result-card {
  border: 1px solid black;
  border-radius: 5px;
  padding: 5px;
}
</style>

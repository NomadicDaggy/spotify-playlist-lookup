<script setup lang="ts">
import {} from "vue";

export interface Track {
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
}

export interface Props {
  track: Track;
}

const props = withDefaults(defineProps<Props>(), {});

props.track; // Track | undefined
</script>

<template>
  <div class="track-result-card">{{ track.name }}</div>
</template>

<style>
.track-result-card {
  border: 1px solid black;
  border-radius: 5px;
  padding: 5px;
}
</style>

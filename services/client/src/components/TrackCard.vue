<script setup lang="ts">
import {} from "vue";
import type { Ref } from "vue";

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
  track: any;
  selected: boolean;
}

const props = defineProps<Props>();

props.track; // Ref<tyepof Track | null>
props.selected; // boolean
</script>

<template>
  <div class="track-result-card" :class="{ selected: selected }">
    <span v-if="track">
      {{ track.name }}
    </span>
    <span v-else>Loading...</span>
  </div>
</template>

<style>
.track-result-card {
  border: 1px solid black;
  border-radius: 5px;
  padding: 5px;
}

.selected {
  border: 1px solid green;
}
</style>

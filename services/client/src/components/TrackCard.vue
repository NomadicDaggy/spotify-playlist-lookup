<script setup lang="ts">
import {} from "vue";

export interface Track {
  name: {
    type: String;
    default: "";
    required: true;
  };
  artistName: {
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
  <div class="track-result-card" :class="{ selected: selected }" v-if="track">
    <span class="track-name">{{ track.name }}</span>
    <span class="track-artist">{{ track.artistName }}</span>
  </div>
  <span v-else>Loading...</span>
</template>

<style>
div.track-result-card {
  padding: 1rem;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
  margin-top: -1px;

  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  cursor: pointer;
}

span.track-name {
  font-size: 1rem;
  line-height: 1;
}

span.track-artist {
  font-size: 0.8rem;
  line-height: 1;
  color: gray;
}

.selected {
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);

  cursor: default;
}

@media only screen and (min-width: 768px) {
  div.track-result-card {
    margin: 0.5rem 0;
    border: 1px solid var(--color-border);
    border-radius: 0.5rem;
  }

  div.track-result-card:hover {
    background-color: var(--green-background);
  }
}
</style>

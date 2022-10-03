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
  spotifyID: {
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
    <span class="track-album">{{ track.albumName }}</span>
  </div>
  <span v-else>Loading...</span>
</template>

<style>
div.track-result-card {
  padding: 1rem;
  border-top: 1px solid gray;

  display: flex;
  flex-direction: column;
  gap: 0.5rem;

  cursor: pointer;
}

div.track-result-card:last-child {
  border-bottom: 1px solid gray;
}

span.track-name {
  font-size: 1rem;
  line-height: 1;
  font-weight: 600;
}

span.track-artist {
  font-size: 0.8rem;
  line-height: 1;
  font-weight: 600;
  color: gray;
}

span.track-album {
  font-size: 0.75rem;
  line-height: 1;
  color: gray;
  padding-top: 0.3rem;
}

div.selected {
  border-top: 1px solid gray;
  border-bottom: 1px solid gray;

  cursor: default;

  margin-top: 0px;
}

@media only screen and (min-width: 768px) {
  div.track-result-card {
    margin: 0.5rem 0;
    border: 1px solid gray;
    border-radius: 0.5rem;
  }

  div.track-result-card:hover {
    background-color: var(--green-background);
  }

  div.selected {
    border-left: none;
    border-radius: 0;

    border-top-right-radius: 0.5rem;
    border-bottom-right-radius: 0.5rem;

    margin: 0;
  }

  div.selected:hover {
    background-color: unset;
  }
}
</style>

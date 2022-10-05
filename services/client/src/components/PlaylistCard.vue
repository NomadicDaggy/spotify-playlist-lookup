<script setup lang="ts">
import {} from "vue";

export interface Playlist {
  name: string;
  spotifyID: string;
  imageURL: string;
  ownerName: string;
  description: string;
  followerCount: string;
  trackCount: string;
}

export interface Props {
  playlist: Playlist;
}

const props = defineProps<Props>();

props.playlist; // Playlist | undefined
</script>

<template>
  <a
    :href="'https://open.spotify.com/playlist/' + playlist.spotifyID"
    target="_blank"
  >
    <div class="playlist-result-card">
      <div>
        <img :src="playlist.imageURL" loading="lazy" class="playlist-image" />
        <div>
          <h2 class="playlist-name">{{ playlist.name }}</h2>
          <span class="playlist-owner">{{ playlist.ownerName }}</span>
          <span class="playlist-stats">
            {{ playlist.followerCount }} likes <span class="dot">/</span>
            {{ playlist.trackCount }} tracks
          </span>
        </div>
      </div>
      <div class="playlist-description" v-if="playlist.description">
        {{ playlist.description }}
      </div>
    </div>
  </a>
</template>

<style>
div.playlist-result-card {
  border-top: 1px solid gray;
  margin-top: -1px;
  padding: 1rem 0;
  cursor: pointer;
  color: var(--color-text);
  background-color: white;
}

div.playlist-result-card:last-child {
  border-bottom: 1px solid gray;
}

div.playlist-result-card > div {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  padding: 0 1rem;
}

div.playlist-result-card > div > div {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

img.playlist-image {
  height: 85px;
  width: 85px;
  object-fit: cover;
  object-position: center;
  margin: 0;
  border-radius: 15px;
  border: 0px transparent;
}

h2.playlist-name {
  font-size: 1.2rem;
  line-height: 1;
}

span.playlist-owner {
  font-size: 1rem;
  line-height: 1;
  font-weight: 500;
}

div.playlist-description {
  font-size: 0.9rem;
  text-align: left;
  line-height: 1;
  margin-top: 1rem;
  color: gray;
}

span.playlist-stats {
  line-height: 1;
  font-size: 0.85rem;
  font-stretch: condensed;
}

span.dot {
  font-weight: 300;
  color: gray;
}

@media only screen and (min-width: 768px) {
  div.playlist-result-card {
    margin-bottom: 1rem;
    border: 1px solid gray;
    border-radius: 1rem;
  }

  div.playlist-result-card:hover {
    background-color: var(--green-background);
  }

  span.playlist-stats {
    padding-top: 1rem;
  }
}
</style>

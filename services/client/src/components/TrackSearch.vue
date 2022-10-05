<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from "vue";
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
const reqPage = ref(1);
const scrollComponent = ref<HTMLElement | null>(null);
const stopLoading = ref(false);
const statusText = ref("Find playlists that contain a specific track");
const tracks = ref<typeof Track | null>(null);

watch(searchTerm, (_) => {
  stopLoading.value = false;
});

const getTracksFromAPI = (url: string, append: boolean) => {
  axios
    .get(url)
    .then((response) => {
      if (response.data["tracks"].length == 0) {
        stopLoading.value = true;
        return;
      }

      let foundTrackCount = response.data["count"];
      statusText.value = `Found ${foundTrackCount} tracks.`;

      if (append && tracks.value) {
        tracks.value = tracks.value.concat(response.data["tracks"]);
      } else {
        tracks.value = response.data["tracks"];
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

const fetchTracks = () => {
  if (!searchTerm.value) {
    statusText.value =
      "Please enter text to search tracks by. It can even be just part of the track name.";
    tracks.value = null;
    router.replace({ name: "tracks" });
    reqPage.value = 0;
    return;
  }

  // add param to url
  router.replace({ name: "tracks", query: { name: searchTerm.value } });

  getTracksFromAPI(
    "http://localhost:1337/api/v1/tracks?name=" + searchTerm.value + "&page=1",
    false
  );
};

const loadMoreTracks = () => {
  if (stopLoading.value == true) {
    console.log("reached end");
    return;
  }

  console.log("loading more tracks");
  getTracksFromAPI(
    "http://localhost:1337/api/v1/tracks?name=" +
      searchTerm.value +
      "&page=" +
      ++reqPage.value,
    true
  );
};

const selectTrack = (track: any) => {
  store.$patch({
    storedTrack: track,
  });

  router.push({
    name: "trackPlaylists",
    params: {
      trackSpotifyID: track.spotifyID,
    },
  });
};

if (searchTerm.value) {
  fetchTracks();
}

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});
onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});
const handleScroll = () => {
  let element = scrollComponent.value;
  if (element == null) {
    return;
  }

  if (element.getBoundingClientRect().bottom < window.innerHeight) {
    loadMoreTracks();
  }
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
    <div class="tracks-container" ref="scrollComponent">
      <TrackCard
        v-for="(track, index) in tracks"
        :track="track"
        :selected="false"
        :index="index"
        :key="track.spotifyID"
        @click="selectTrack(track)"
      />
    </div>
  </div>
</template>

<style>
input.track-name-input {
  max-width: 80vw;
  height: 2rem;
  border: 1px solid gray;
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
    border-bottom: none;
  }
}
</style>

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

const reqPage = ref(1);
const scrollComponent = ref<HTMLElement | null>(null);
const stopLoading = ref(false);

const defaultText = "";
const statusText = ref(defaultText);

const trackCount = ref("");
const playlistCount = ref("");

axios.get("http://localhost:1337/api/v1/simple-stats").then((response) => {
  trackCount.value = response.data["trackCount"];
  playlistCount.value = response.data["playlistCount"];
});

const searchTerm = ref(route.query.name);

watch(searchTerm, (_) => {
  stopLoading.value = false;
});

const tracks = ref<typeof Track | null>(null);

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
    statusText.value = defaultText;
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
    return;
  }

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
    <div class="stats-counter">
      Find one of
      <span class="site-statistic">{{ playlistCount }}</span> Spotify playlists
      <br />
      by entering one of
      <span class="site-statistic">{{ trackCount }}</span> tracks you want the
      playlist to contain
    </div>
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

<style scoped>
div.stats-counter {
  text-align: center;
  line-height: 1.2;
  padding-bottom: 2rem;
  font-weight: 400;
}

span.site-statistic {
  font-weight: 700;
}

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
  line-height: 1.15;
}

@media only screen and (min-width: 768px) {
  div.tracks-container {
    max-width: 600px;
    margin: 0 auto;
    border-bottom: none;
  }

  div.stats-counter {
    font-size: 1.2rem;
  }
}
</style>

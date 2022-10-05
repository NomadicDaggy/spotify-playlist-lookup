<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";
import PlaylistCard from "../components/PlaylistCard.vue";
import { useTrackStore } from "../stores/track";
import { storeToRefs } from "pinia";
import TrackCard from "../components/TrackCard.vue";

const reqPage = ref(1);
const scrollComponent = ref<HTMLElement | null>(null);
const stopLoading = ref(false);

const router = useRouter();
const route = useRoute();

const store = useTrackStore();
const { storedTrack } = storeToRefs(store);

const playlists = ref();
const getPlaylistsFromAPI = (url: string, append: boolean) => {
  axios
    .get(url)
    .then((response) => {
      if (response.data["playlists"].length == 0) {
        stopLoading.value = true;
        return;
      }

      if (append && playlists.value) {
        playlists.value = playlists.value.concat(response.data["playlists"]);
      } else {
        playlists.value = response.data["playlists"];
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

if (storedTrack.value) {
  getPlaylistsFromAPI(
    "http://localhost:1337/api/v1/tracks/" +
      storedTrack.value?.spotifyID +
      "/playlists?page=1",
    false
  );
} else {
  // If no value in pinia store, then the user has come here without first selecting a track,
  // rather they just followed a link straight to this page.
  // So we need to get the track from the url parameter from our backend api
  axios
    .get(
      "http://localhost:1337/api/v1/tracks?spotifyID=" +
        route.params.trackSpotifyID
    )
    .then((response) => {
      store.$patch({
        storedTrack: response.data,
      });
      getPlaylistsFromAPI(
        "http://localhost:1337/api/v1/tracks/" +
          storedTrack.value?.spotifyID +
          "/playlists?page=1",
        false
      );
    })
    .catch((error) => {
      console.log(error);
    });
}

const loadMorePlaylists = () => {
  if (stopLoading.value == true) {
    console.log("reached end");
    return;
  }

  console.log("loading more tracks");
  getPlaylistsFromAPI(
    "http://localhost:1337/api/v1/tracks/" +
      storedTrack.value?.spotifyID +
      "/playlists?page=" +
      ++reqPage.value,
    true
  );
};

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
    loadMorePlaylists();
  }
};
</script>

<template>
  <div class="playlist-results-container">
    <div>
      <div class="track-selected-note">Selected track:</div>
      <div class="track-span">
        <div @click="router.go(-1)" class="back-button-div">
          <v-icon name="io-chevron-back-outline" class="back-button" />
        </div>
        <div class="track-card-container">
          <TrackCard v-if="storedTrack" :track="storedTrack" :selected="true" />
          <div v-else>Loading...</div>
        </div>
      </div>
    </div>

    <div class="playlists-container" v-if="playlists" ref="scrollComponent">
      <span class="status-text">Playlists containing selected track:</span>
      <PlaylistCard
        v-for="(playlist, index) in playlists"
        :playlist="playlist"
        :index="index"
        :key="playlist.spotifyID"
      />
    </div>
    <div v-else>Loading...</div>
  </div>
</template>

<style>
div.playlist-results-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

div.track-selected-note {
  width: 100%;
  text-align: center;
}

div.track-span {
  display: flex;
  flex-direction: row;
}

div.track-card-container {
  width: 100%;
}

div.back-button-div {
  background-color: var(--color-background-mute);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-width: 4rem;
  cursor: pointer;
  border: 1px solid gray;
  border-right: 0;
  border-left: 0;
}

.back-button {
  width: 2rem;
  height: 2rem;
}

span.status-text {
  text-align: center;
  display: block;
  padding-top: 1rem;
  padding-bottom: 0rem;
}

@media only screen and (min-width: 768px) {
  div.playlist-results-container {
    width: 700px;
    margin: 0 auto;
    border-bottom: none;
  }

  div.back-button-div {
    border-top-left-radius: 0.5rem;
    border-bottom-left-radius: 0.5rem;
    border: 1px solid gray;
    border-right: 0;
  }

  div.back-button-div:hover {
    background-color: var(--green-background);
  }
}
</style>

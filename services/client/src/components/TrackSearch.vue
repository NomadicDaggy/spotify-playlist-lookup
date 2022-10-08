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
const noTrackText = "We don't have this track, try a different one!";
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
      let foundTrackCount = response.data["count"];

      if (foundTrackCount == 0 && append) {
        stopLoading.value = true;
        return;
      }

      if (foundTrackCount > 0) {
        statusText.value = `Found ${foundTrackCount} tracks.`;
      } else {
        statusText.value = noTrackText;
      }

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

const droppedTrack = ref<typeof Track | null>(null);

function getSpecificTrack(spotifyID: string) {
  return axios
    .get("http://localhost:1337/api/v1/tracks?spotifyID=" + spotifyID)
    .then((response) => {
      if (response.status == 200) {
        droppedTrack.value = response.data;
      }
    })
    .catch(() => {
      statusText.value = noTrackText;
      console.clear(); // chrome shows error in console
    });
}

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

watch(droppedTrack, (_) => {
  selectTrack(droppedTrack.value);
});

if (searchTerm.value) {
  fetchTracks();
}

const handleScroll = () => {
  let element = scrollComponent.value;
  if (element == null) {
    return;
  }

  if (element.getBoundingClientRect().bottom < window.innerHeight) {
    loadMoreTracks();
  }
};

var dropZone: HTMLElement | null = null;

function showDropZone() {
  if (dropZone) {
    dropZone.style.display = "block";
  }
}
function hideDropZone() {
  if (dropZone) {
    dropZone.style.display = "none";
  }
}
function allowDrag(e: Event) {
  let c = true;
  if (c) {
    // Test that the item being dragged is a valid one
    e.preventDefault();
  }
}
function handleDrop(e: DragEvent) {
  e.preventDefault();
  hideDropZone();

  let failText =
    "Spotify track link should look like 'https://open.spotify.com/track/22numbersOrLetters'";

  if (!e.dataTransfer) {
    statusText.value = failText;
    return;
  }

  let t = e.dataTransfer.getData("Text");
  // in case link is in form 'https://open.spotify.com/track/3rmo8F54jFF8OgYsqTxm5d?si=c9a79044c8354ff0'
  // or has any other url query
  t = t.split("?")[0];

  let spotifyLinkPrefix = "https://open.spotify.com/track/";
  if (!t.startsWith(spotifyLinkPrefix)) {
    statusText.value = failText;
    return;
  }

  let trackSpotifyID = t.split("/").at(-1); // ignore error
  if (!(trackSpotifyID.length == 22)) {
    statusText.value = failText;
    return;
  }

  getSpecificTrack(trackSpotifyID);
}

onMounted(() => {
  window.addEventListener("scroll", handleScroll);

  dropZone = document.getElementById("dropzone");

  if (dropZone) {
    window.addEventListener("dragenter", showDropZone);
    dropZone.addEventListener("dragenter", allowDrag);
    dropZone.addEventListener("dragover", allowDrag);
    dropZone.addEventListener("dragleave", hideDropZone);
    dropZone.addEventListener("drop", handleDrop);
  }
});
onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
  window.removeEventListener("dragenter", allowDrag);
  window.removeEventListener("dragover", allowDrag);
  window.removeEventListener("dragleave", hideDropZone);
  window.removeEventListener("drop", handleDrop);
});
</script>

<template>
  <div id="dropzone" class="dropzone"></div>
  <div class="track-search-container">
    <div class="stats-counter">
      Currently we keep track of
      <span class="site-statistic">{{ playlistCount }}</span> Spotify playlists
      and <span class="site-statistic">{{ trackCount }}</span> tracks.
    </div>
    <div class="enter-prompt">
      <span>Enter a track name to find playlists that contain it.</span>
      <span class="drag-drop-info">
        <br />
        Or drag the track from Spotify and drop anywhere.
      </span>
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
div.dropzone {
  box-sizing: border-box;
  display: none;
  position: fixed;
  width: 100%;
  height: 100%;
  left: 0;
  top: 0;
  z-index: 99999;

  background: var(--green-background);
}

div.stats-counter {
  text-align: center;
  line-height: 1.2;
  padding-bottom: 2rem;
  font-weight: 400;
}

span.site-statistic {
  font-weight: 700;
}

div.enter-prompt {
  text-align: center;
  padding-bottom: 1rem;
  line-height: 1.2;
}
span.drag-drop-info {
  display: none;
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

  span.drag-drop-info {
    display: inline;
  }
}
</style>

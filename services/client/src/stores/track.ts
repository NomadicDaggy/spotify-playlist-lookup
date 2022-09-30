import { ref } from "vue";
import { defineStore } from "pinia";
import type Ref from 'vue';
import type Track from "../components/TrackCard.vue";

export const useTrackStore = defineStore("track", () => {
  const storedTrack = ref<typeof Track>();

  return { storedTrack };
});

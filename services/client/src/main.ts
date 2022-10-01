import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import { OhVueIcon, addIcons } from "oh-vue-icons";
import { IoChevronBackOutline } from "oh-vue-icons/icons";

import TrackSearch from "./components/TrackSearch.vue";
import TrackCard from "./components/TrackCard.vue";
import PlaylistCard from "./components/PlaylistCard.vue";

import "./assets/main.css";

const app = createApp(App);

addIcons(IoChevronBackOutline);

app.use(createPinia());
app.use(router);

app.component("TrackSearch", TrackSearch);
app.component("TrackCard", TrackCard);
app.component("PlaylistCard", PlaylistCard);
app.component("v-icon", OhVueIcon);

app.mount("#app");

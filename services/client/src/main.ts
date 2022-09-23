import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import TrackSearch from "./components/TrackSearch.vue";

import "./assets/main.css";

const app = createApp(App);

app.use(createPinia());
app.use(router);

app.component("TrackSearch", TrackSearch);

app.mount("#app");

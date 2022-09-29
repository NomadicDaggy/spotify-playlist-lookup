import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import TrackPlaylists from "../views/TrackPlaylists.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/tracks",
      name: "tracks",
      alias: "/",
      component: HomeView,
    },
    {
      path: "/tracks/:trackSpotifyID/playlists",
      name: "trackPlaylists",
      component: TrackPlaylists,
      props: true,
    },
    {
      path: "/about",
      name: "about",
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import("../views/AboutView.vue"),
    },
  ],
});

export default router;

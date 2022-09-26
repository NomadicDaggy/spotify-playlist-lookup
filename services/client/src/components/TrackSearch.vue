<script setup lang="ts">
import { ref } from "vue";
import axios from "axios";

const searchTerm = ref("");

const fetchTracks = () => {
  axios
    .get("http://localhost:1337/api/v1/tracks?name=" + searchTerm.value)
    .then((response) => {
      console.log(response.data);
    })
    .catch((error) => {
      console.log(error);
    });
};

function getTracks() {
  console.log(searchTerm.value);
  fetchTracks();
}
</script>

<template>
  <div class="track-search-container">
    <input v-model="searchTerm" @keyup.enter="getTracks" />
  </div>
</template>

<style>
input {
  min-width: 250px;
  margin: 20px auto;
  display: block;
}
</style>

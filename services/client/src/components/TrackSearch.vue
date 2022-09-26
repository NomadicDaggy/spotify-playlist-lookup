<script setup lang="ts">
import { ref } from "vue";

const searchTerm = ref("");

function logSearch() {
  console.log(searchTerm.value);
}
</script>

<template>
  <div class="track-search-container">
    <input v-model="searchTerm" @keyup.enter="logSearch" />
  </div>
</template>

<style>
input {
  min-width: 250px;
  margin: 20px auto;
  display: block;
}
</style>

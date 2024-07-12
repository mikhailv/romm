<script setup lang="ts">
import { ref } from "vue";

// Props
const emitter = useNuxtApp().$emitter;
const isShowSortBar = ref(false);
function showSortBar() {
  emitter?.emit("sortBarShow", null);
  isShowSortBar.value = !isShowSortBar.value;
}
</script>

<template>
  <v-tooltip
    location="bottom"
    class="tooltip"
    text="Order gallery"
    transition="fade-transition"
    open-delay="1000"
  >
    <template #activator="{ props }">
      <v-btn
        class="ml-0"
        variant="text"
        rounded="0"
        icon="mdi-sort"
        v-bind="props"
        :color="isShowSortBar ? 'romm-accent-1' : ''"
        @click="showSortBar" /></template
  ></v-tooltip>
</template>

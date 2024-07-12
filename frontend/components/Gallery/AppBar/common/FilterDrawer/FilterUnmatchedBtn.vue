<script setup lang="ts">
import storeGalleryFilter from "@/stores/galleryFilter";
import { storeToRefs } from "pinia";

// Props
const galleryFilterStore = storeGalleryFilter();
const { filterUnmatched } = storeToRefs(galleryFilterStore);
const emitter = useNuxtApp().$emitter;
function setUnmatched() {
  galleryFilterStore.switchFilterUnmatched();
  emitter?.emit("filter", null);
}
</script>

<template>
  <v-btn
    block
    variant="tonal"
    rounded="0"
    :color="filterUnmatched ? 'romm-accent-1' : 'romm-gray'"
    @click="setUnmatched()"
  >
    <v-icon :color="filterUnmatched ? 'romm-accent-1' : 'romm-white'"
      >mdi-file-find-outline</v-icon
    ><span
      class="ml-2"
      :class="{
        'text-romm-white': !filterUnmatched,
        'text-romm-accent-1': filterUnmatched,
      }"
      >Filter unmatched</span
    ></v-btn
  >
</template>

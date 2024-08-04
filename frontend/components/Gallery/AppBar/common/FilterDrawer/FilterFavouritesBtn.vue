<script setup lang="ts">
import storeGalleryFilter from "@/stores/galleryFilter";
import { storeToRefs } from "pinia";

// Props
const galleryFilterStore = storeGalleryFilter();
const { filterFavourites } = storeToRefs(galleryFilterStore);
const emitter = useNuxtApp().$emitter;
function setFavourites() {
  galleryFilterStore.switchFilterFavourites();
  emitter?.emit("filter", null);
}
</script>

<template>
  <v-btn
    block
    variant="tonal"
    rounded="0"
    :color="filterFavourites ? 'romm-accent-1' : 'romm-gray'"
    @click="setFavourites()"
  >
    <v-icon :color="filterFavourites ? 'romm-accent-1' : 'romm-white'">
      mdi-star
    </v-icon><span
      class="ml-2"
      :class="{
        'text-romm-white': !filterFavourites,
        'text-romm-accent-1': filterFavourites,
      }"
    >Filter favourites</span>
  </v-btn>
</template>

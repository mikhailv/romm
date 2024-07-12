<script setup lang="ts">
import storeGalleryFilter from "@/stores/galleryFilter";
import { debounce } from "lodash";
import { storeToRefs } from "pinia";
import { nextTick } from "vue";

// Props
const emitter = useNuxtApp().$emitter;
const galleryFilterStore = storeGalleryFilter();
const { filterSearch } = storeToRefs(galleryFilterStore);

// Functions
const filterRoms = debounce(() => {
  emitter?.emit("filter", null);
}, 500);

function clear() {
  filterSearch.value = "";
}
</script>

<template>
  <v-text-field
    v-model="filterSearch"
    prepend-inner-icon="mdi-filter-outline"
    label="Filter"
    rounded="0"
    hide-details
    clearable
    @click:clear="clear"
    @update:model-value="nextTick(filterRoms)"
  />
</template>

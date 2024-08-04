<script setup lang="ts">
import storeGalleryFilter from "@/stores/galleryFilter";
import { storeToRefs } from "pinia";
import { nextTick, ref } from "vue";

// Props
const emitter = useNuxtApp().$emitter;
const galleryFilterStore = storeGalleryFilter();
const {
  activeFilterDrawer,
  selectedGenre,
  filterGenres,
  selectedFranchise,
  filterFranchises,
  selectedCollection,
  filterCollections,
  selectedCompany,
  filterCompanies,
} = storeToRefs(galleryFilterStore);
const filters = [
  {
    label: "Genre",
    selected: selectedGenre,
    items: filterGenres,
  },
  {
    label: "Franchise",
    selected: selectedFranchise,
    items: filterFranchises,
  },
  {
    label: "Collection",
    selected: selectedCollection,
    items: filterCollections,
  },
  {
    label: "Company",
    selected: selectedCompany,
    items: filterCompanies,
  },
];

// Functions
function resetFilters() {
  selectedGenre.value = null;
  selectedFranchise.value = null;
  selectedCollection.value = null;
  selectedCompany.value = null;
  galleryFilterStore.disableFilterUnmatched();
  galleryFilterStore.disableFilterFavourites();
  nextTick(() => emitter?.emit("filter", null));
}
</script>

<template>
  <v-navigation-drawer
    v-model="activeFilterDrawer"
    floating
    width="300"
    mobile
    @update:model-value="galleryFilterStore.switchActiveFilterDrawer()"
  >
    <v-list>
      <v-list-item>
        <gallery-app-bar-common-filter-drawer-filter-unmatched-btn />
        <gallery-app-bar-common-filter-drawer-filter-favourites-btn
          class="mt-2"
        />
      </v-list-item>
      <v-list-item v-for="filter in filters">
        <v-autocomplete
          v-model="filter.selected.value"
          rounded="0"
          hide-details
          clearable
          :label="filter.label"
          variant="solo-filled"
          density="comfortable"
          :items="filter.items.value"
          @update:model-value="nextTick(() => emitter?.emit('filter', null))"
        />
      </v-list-item>
      <v-list-item class="justify-center d-flex">
        <v-btn
          size="small"
          variant="tonal"
          @click="resetFilters"
        >
          Reset filters
        </v-btn>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

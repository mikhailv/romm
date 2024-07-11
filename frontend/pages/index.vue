<script setup lang="ts">
import romApi from "@/services/api/rom";
import storeCollections from "@/stores/collections";
import storePlatforms from "@/stores/platforms";
import storeRoms from "@/stores/roms";
import { storeToRefs } from "pinia";
import { onMounted } from "vue";

// Props
const romsStore = storeRoms();
const { recentRoms } = storeToRefs(romsStore);
const platforms = storePlatforms();
const { filledPlatforms } = storeToRefs(platforms);
const collections = storeCollections();
const { allCollections } = storeToRefs(collections);

// Functions
onMounted(async () => {
  await romApi
    .getRecentRoms()
    .then(({ data: recentData }) => {
      romsStore.setRecentRoms(recentData);
    })
    .catch((error) => {
      console.error(error);
    });
});
</script>

<template>
  <dashboard-stats />
  <dashboard-recent v-if="recentRoms.length > 0" />
  <dashboard-platforms v-if="filledPlatforms.length > 0" />
  <dashboard-collections v-if="allCollections.length > 0" />
</template>

<script setup lang="ts">
import storeNavigation from "@/stores/navigation";
import { storeToRefs } from "pinia";

// Props
const navigationStore = storeNavigation();
const { activePlatformsDrawer, activeCollectionsDrawer, activeSettingsDrawer } =
  storeToRefs(navigationStore);
</script>
<template>
  <v-navigation-drawer
    permanent
    rail
    :floating="
      activePlatformsDrawer || activeCollectionsDrawer || activeSettingsDrawer
    "
    rail-width="60"
  >
    <template #prepend>
      <v-row
        no-gutters
        class="my-2 justify-center"
      >
        <navigation-home-btn />
      </v-row>
    </template>

    <v-divider
      opacity="0"
      class="my-4"
    />
    <navigation-search-btn block />
    <navigation-platforms-btn block />
    <navigation-collections-btn block />
    <v-divider
      opacity="0"
      class="my-3"
    />
    <navigation-upload-btn block />
    <navigation-scan-btn block />
    <template #append>
      <v-row
        no-gutters
        class="my-2 justify-center"
      >
        <navigation-user-btn />
      </v-row>
    </template>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { inject } from "vue";
import { useRoute } from "vue-router";


import storePlatforms, { type Platform } from "@/stores/platforms";

// Props
const emitter = useNuxtApp().$emitter;
const platforms = storePlatforms();
const route = useRoute();
</script>

<template>
  <v-list-item
    v-if="route.params.platform"
    class="py-4 pr-5"
    @click="
      emitter?.emit(
        'showUploadRomDialog',
        platforms.get(Number(route.params.platform)) as Platform
      )
    "
  >
    <v-list-item-title class="d-flex">
      <v-icon
        icon="mdi-upload"
        class="mr-2"
      />Upload roms
    </v-list-item-title>
  </v-list-item>
</template>

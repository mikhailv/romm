<script setup lang="ts">
import { type Collection } from "@/stores/collections";
import storeRoms from "@/stores/roms";
import { useRoute } from "vue-router";

// Props
const emitter = useNuxtApp().$emitter;
const route = useRoute();
const roms = storeRoms();
</script>

<template>
  <v-list-item
    v-if="route.params.id"
    class="py-4 pr-5 text-romm-red"
    @click="
      emitter?.emit(
        'showDeleteCollectionDialog',
        roms.currentCollection as Collection
      )
    "
  >
    <v-list-item-title class="d-flex">
      <v-icon
        icon="mdi-delete"
        color="red"
        class="mr-2"
      />
      Delete collection
    </v-list-item-title>
  </v-list-item>
</template>

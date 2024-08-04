<script setup lang="ts">
import storeCollections from "@/stores/collections";
import { views } from "@/utils";

// Props
const collections = storeCollections();
</script>
<template>
  <common-r-section
    icon="mdi-bookmark-box-multiple"
    title="Collections"
  >
    <template #content>
      <v-row no-gutters>
        <v-col
          v-for="collection in collections.allCollections"
          :key="collection.name"
          class="pa-1"
          :cols="views[0]['size-cols']"
          :sm="views[0]['size-sm']"
          :md="views[0]['size-md']"
          :lg="views[0]['size-lg']"
          :xl="views[0]['size-xl']"
        >
          <common-collection-card
            :key="collection.updated_at"
            show-rom-count
            show-title
            transform-scale
            :collection="collection"
          />
        </v-col>
      </v-row>
    </template>
  </common-r-section>
</template>

<script setup lang="ts">
import storeCollections from "@/stores/collections";
import storeNavigation from "@/stores/navigation";
import { storeToRefs } from "pinia";
import { useDisplay } from "vuetify";

// Props
const navigationStore = storeNavigation();
const { smAndDown } = useDisplay();
const collectionsStore = storeCollections();
const { filteredCollections, searchText } = storeToRefs(collectionsStore);
const { activeCollectionsDrawer } = storeToRefs(navigationStore);
const emitter = useNuxtApp().$emitter;

// Functions
async function addCollection() {
  emitter?.emit("showCreateCollectionDialog", null);
}

function clear() {
  searchText.value = "";
}
</script>
<template>
  <v-navigation-drawer
    v-model="activeCollectionsDrawer"
    :location="smAndDown ? 'top' : 'left'"
    mobile
    width="400"
    class="bg-terciary"
  >
    <template #prepend>
      <v-text-field
        v-model="searchText"
        prepend-inner-icon="mdi-filter-outline"
        clearable
        hide-details
        single-line
        label="Search collection"
        variant="solo-filled"
        rounded="0"
        @click:clear="clear"
        @update:model-value=""
      />
    </template>
    <v-list
      lines="two"
      rounded="0"
      class="pa-0"
    >
      <common-collection-list-item
        v-for="collection in filteredCollections"
        :collection="collection"
      />
    </v-list>
    <template #append>
      <v-btn
        variant="tonal"
        color="romm-accent-1"
        prepend-icon="mdi-plus"
        size="large"
        rounded="0"
        block
        @click="addCollection()"
      >
        Add Collection
      </v-btn>
    </template>
  </v-navigation-drawer>
</template>

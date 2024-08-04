<script setup lang="ts">
import storeAuth from "@/stores/auth";

// Props
const auth = storeAuth();
</script>

<template>
  <v-app-bar
    id="gallery-app-bar"
    elevation="0"
    density="compact"
  >
    <gallery-app-bar-platform-firmware-btn />
    <gallery-app-bar-common-filter-btn />
    <gallery-app-bar-common-filter-text-field />
    <gallery-app-bar-common-selecting-btn />
    <gallery-app-bar-common-gallery-view-btn />
    <v-menu location="bottom">
      <template #activator="{ props }">
        <v-btn
          v-if="auth.scopes.includes('roms.write')"
          v-bind="props"
          rounded="0"
          variant="text"
          class="mr-0"
          icon="mdi-dots-vertical"
          @click.stop
        />
      </template>
      <gallery-app-bar-platform-admin-menu />
    </v-menu>
  </v-app-bar>

  <gallery-app-bar-common-filter-drawer />
  <gallery-app-bar-platform-firmware-drawer />
</template>

<style scoped>
#gallery-app-bar {
  z-index: 999 !important;
}
</style>

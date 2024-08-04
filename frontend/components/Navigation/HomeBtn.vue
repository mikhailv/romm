<script setup lang="ts">
import storeNavigation from "@/stores/navigation";

// Props
const navigationStore = storeNavigation();
</script>
<template>
  <v-hover v-slot="{ isHovering, props: hoverProps }">
    <common-romm-iso
      v-bind="hoverProps"
      class="pointer"
      :class="{ 'border-romm-accent-1': isHovering }"
      :size="35"
      @click="navigationStore.goHome"
    />
  </v-hover>
</template>

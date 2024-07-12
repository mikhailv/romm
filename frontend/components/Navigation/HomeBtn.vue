<script setup lang="ts">
import storeNavigation from "@/stores/navigation";

// Props
const navigationStore = storeNavigation();
</script>
<template>
  <v-hover v-slot="{ isHovering, props: hoverProps }">
    <common-romm-iso
      @click="navigationStore.goHome"
      v-bind="hoverProps"
      class="pointer"
      :class="{ 'border-romm-accent-1': isHovering }"
      :size="35"
    />
  </v-hover>
</template>

<script setup lang="ts">
import { ref } from "vue";
import RommIso from "@/components/common/RommIso.vue";
import storeNavigation from "@/stores/navigation";

const homeUrl = ref(`${location.protocol}//${location.host}`);
const navigationStore = storeNavigation();
</script>
<template>
  <a
    @click.prevent
    style="text-decoration: none; color: inherit"
    :href="homeUrl"
  >
    <romm-iso
      @click="navigationStore.goHome"
      class="pointer romm-iso"
      :size="35"
    />
  </a>
</template>

<style lang="scss" scoped>
.romm-iso {
  transition: filter 0.15s ease-in-out;
}

.romm-iso:hover {
  filter: drop-shadow(0px 0px 2px #a452fe);
}
</style>

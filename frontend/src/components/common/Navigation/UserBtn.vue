<script setup lang="ts">
import storeAuth from "@/stores/auth";
import storeNavigation from "@/stores/navigation";
import { defaultAvatarPath } from "@/utils";
import { storeToRefs } from "pinia";

// Props
const navigationStore = storeNavigation();
const auth = storeAuth();
const { user } = storeToRefs(auth);
</script>
<template>
  <v-avatar
    @click="navigationStore.switchActiveSettingsDrawer"
    class="pointer"
    size="35"
  >
    <v-img
      :src="
        user?.avatar_path
          ? `/assets/romm/assets/${user?.avatar_path}?ts=${user?.updated_at}`
          : defaultAvatarPath
      "
    />
  </v-avatar>
</template>

<style lang="scss" scoped>
.v-avatar {
  transition: filter 0.15s ease-in-out;
}

.v-avatar:hover {
  filter: drop-shadow(0px 0px 2px #a452fe);
}
</style>

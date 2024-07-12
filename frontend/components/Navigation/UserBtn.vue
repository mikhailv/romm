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
  <v-hover v-slot="{ isHovering, props: hoverProps }">
    <v-avatar
      @click="navigationStore.switchActiveSettingsDrawer"
      class="pointer"
      size="35"
      v-bind="hoverProps"
      :class="{ 'border-romm-accent-1': isHovering }"
    >
      <!-- TODO: nuxt3 not rendering dynamic src -->
      <v-img
        :src="
          user?.avatar_path
            ? `/assets/${user?.avatar_path}?ts=${user?.updated_at}`
            : defaultAvatarPath
        "
      >
        <template #error>
          <!-- TODO: not working with variable -->
          <!-- <v-img :src="defaultAvatarPath" /> -->
          <v-img :src="`/images/default/user.png`" />
        </template>
      </v-img>
    </v-avatar>
  </v-hover>
</template>

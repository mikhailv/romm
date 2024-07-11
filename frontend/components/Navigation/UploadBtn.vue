<script setup lang="ts">
import storeAuth from "@/stores/auth";

// Props
const emitter = useNuxtApp().$emitter;
const auth = storeAuth();
</script>
<template>
  <v-btn
    v-if="auth.scopes.includes('roms.write')"
    icon="mdi-upload"
    variant="flat"
    rounded="0"
    @click="emitter?.emit('showUploadRomDialog', null)"
  />
</template>

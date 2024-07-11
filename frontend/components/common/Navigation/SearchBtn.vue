<script setup lang="ts">
const emitter = useNuxtApp().$emitter;
</script>
<template>
  <v-btn
    icon="mdi-magnify"
    variant="flat"
    rounded="0"
    @click="emitter?.emit('showSearchRomDialog', null)"
  />
</template>

<script setup lang="ts">
withDefaults(defineProps<{ size?: number }>(), { size: 40 });
</script>

<template>
  <v-avatar :size="size">
    <img src="/images/isotipo.svg" />
  </v-avatar>
</template>

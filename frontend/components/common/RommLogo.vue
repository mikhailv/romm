<script setup lang="ts">
withDefaults(defineProps<{ size?: number }>(), { size: 40 });
</script>

<template>
  <v-avatar :size="size">
    <v-img src="/images/logotipo.svg" />
  </v-avatar>
</template>

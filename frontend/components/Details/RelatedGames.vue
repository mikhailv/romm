<script setup lang="ts">
import type { DetailedRom } from "@/stores/roms";
import { ref } from "vue";

const props = defineProps<{ rom: DetailedRom }>();
const combined = ref([
  ...(props.rom.igdb_metadata?.remakes ?? []),
  ...(props.rom.igdb_metadata?.remasters ?? []),
  ...(props.rom.igdb_metadata?.expanded_games ?? []),
]);
</script>
<template>
  <v-row no-gutters>
    <v-col cols="4" sm="3" md="6" v-for="rom in combined">
      <common-game-card-related-card :rom="rom" />
    </v-col>
  </v-row>
</template>

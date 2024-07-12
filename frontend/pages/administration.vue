<script setup lang="ts">
import storeAuth from "@/stores/auth";

// Props
const auth = storeAuth();
</script>
<template>
  <administration-users-table />
  <administration-tasks v-if="auth.scopes.includes('tasks.run')" />
</template>

<script setup lang="ts">
import UsersTable from "@/components/Administration/Users/Table.vue";
import Tasks from "@/layouts/Administration/Tasks.vue";
import ApiKeys from "@/layouts/Administration/ApiKeys.vue";
import storeAuth from "@/stores/auth";

// Props
const auth = storeAuth();
</script>
<template>
  <users-table />
  <tasks v-if="auth.scopes.includes('tasks.run')" />
  <api-keys />
</template>

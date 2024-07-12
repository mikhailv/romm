<script setup lang="ts">
import storeNotifications from "@/stores/notifications";
import type { SnackbarStatus } from "@/types/emitter";
import { storeToRefs } from "pinia";

// Props
const notificationStore = storeNotifications();
const { notifications } = storeToRefs(notificationStore);
const emitter = useNuxtApp().$emitter;
emitter?.on("snackbarShow", (snackbar: SnackbarStatus) => {
  snackbar.id = notificationStore.notifications.length + 1;
  notificationStore.add(snackbar);
});
</script>
<template>
  <common-notification
    v-for="notification in notifications"
    :style="{
      'margin-top': `${(notifications.indexOf(notification) + 1) * 60}px`,
    }"
  />
</template>
<style scoped></style>

<script setup lang="ts">
import { ref } from "vue";
import { useDisplay } from "vuetify";

// Props
const { lgAndUp } = useDisplay();
const show = ref(false);
const link = ref("");
const emitter = useNuxtApp().$emitter;
emitter?.on("showCopyDownloadLinkDialog", (downloadLink) => {
  show.value = true;
  link.value = downloadLink;
});

// Functions
function closeDialog() {
  show.value = false;
  link.value = "";
}
</script>

<template>
  <common-r-dialog
    v-model="show"
    icon="mdi-content-copy"
    :width="lgAndUp ? '60vw' : '95vw'"
    @close="closeDialog"
  >
    <template #content>
      <v-row
        class="justify-center text-center pa-2"
        no-gutters
      >
        <v-list-item>
          Can't copy link to clipboard, copy it manually:
        </v-list-item>
      </v-row>
      <v-row
        class="justify-center text-center pa-2 mb-3"
        no-gutters
      >
        <v-list-item class="bg-terciary">
          {{ link }}
        </v-list-item>
      </v-row>
    </template>
  </common-r-dialog>
</template>

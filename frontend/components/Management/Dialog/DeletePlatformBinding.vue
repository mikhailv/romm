<script setup lang="ts">
import configApi from "@/services/api/config";
import storeConfig from "@/stores/config";
import { ref } from "vue";
import { useDisplay } from "vuetify";

// Props
const { lgAndUp } = useDisplay();
const show = ref(false);
const emitter = useNuxtApp().$emitter;
const configStore = storeConfig();
const platformBindingFSSlugToDelete = ref();
const platformBindingSlugToDelete = ref();
emitter?.on("showDeletePlatformBindingDialog", ({ fsSlug, slug }) => {
  platformBindingFSSlugToDelete.value = fsSlug;
  platformBindingSlugToDelete.value = slug;
  show.value = true;
});

// Functions
function deleteBindPlatform() {
  configApi
    .deletePlatformBindConfig({ fsSlug: platformBindingFSSlugToDelete.value })
    .then(() => {
      configStore.removePlatformBinding(platformBindingFSSlugToDelete.value);
    })
    .catch(({ response, message }) => {
      emitter?.emit("snackbarShow", {
        msg: `${response?.data?.detail || response?.statusText || message}`,
        icon: "mdi-close-circle",
        color: "red",
        timeout: 4000,
      });
    });
  closeDialog();
}

function closeDialog() {
  show.value = false;
}
</script>
<template>
  <common-r-dialog
    v-model="show"
    icon="mdi-delete"
    :width="lgAndUp ? '45vw' : '95vw'"
    @close="closeDialog"
  >
    <template #content>
      <v-row
        class="justify-center pa-2 align-center"
        no-gutters
      >
        <span class="mr-1">Deleting platform binding</span>
        <common-platform-icon
          :key="platformBindingSlugToDelete"
          class="mx-2"
          :slug="platformBindingSlugToDelete"
        />
        <span>[</span>
        <span class="text-romm-accent-1 ml-1">
          {{ platformBindingFSSlugToDelete }}</span>
        <span class="mx-1">:</span>
        <span class="text-romm-accent-1">{{
          platformBindingSlugToDelete
        }}</span>
        <span class="ml-1">].</span>
        <span class="ml-1">Do you confirm?</span>
      </v-row>
    </template>
    <template #append>
      <v-row
        class="justify-center mb-2"
        no-gutters
      >
        <v-btn-group
          divided
          density="compact"
        >
          <v-btn
            class="bg-terciary"
            @click="closeDialog"
          >
            Cancel
          </v-btn>
          <v-btn
            class="bg-terciary text-romm-red"
            @click="deleteBindPlatform"
          >
            Confirm
          </v-btn>
        </v-btn-group>
      </v-row>
    </template>
  </common-r-dialog>
</template>

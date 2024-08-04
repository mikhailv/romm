<script setup lang="ts">
import platformApi from "@/services/api/platform";
import storePlatforms, { type Platform } from "@/stores/platforms";
import { ref } from "vue";
import { useDisplay } from "vuetify";

// Props
const router = useRouter();
const { lgAndUp } = useDisplay();
const platformsStore = storePlatforms();
const platform = ref<Platform | null>(null);
const show = ref(false);
const emitter = useNuxtApp().$emitter;
emitter?.on("showDeletePlatformDialog", (platformToDelete) => {
  platform.value = platformToDelete;
  show.value = true;
});

// Functions
async function deletePlatform() {
  if (!platform.value) return;

  show.value = false;
  await platformApi
    .deletePlatform({ platform: platform.value })
    .then((response) => {
      emitter?.emit("snackbarShow", {
        msg: response.data.msg,
        icon: "mdi-check-bold",
        color: "green",
      });
    })
    .catch((error) => {
      console.log(error);
      emitter?.emit("snackbarShow", {
        msg: error.response.data.detail,
        icon: "mdi-close-circle",
        color: "red",
      });
      return;
    });

  await router.push({ name: "index" });

  platformsStore.remove(platform.value);
  emitter?.emit("refreshDrawer", null);
  closeDialog();
}

function closeDialog() {
  show.value = false;
}
</script>
<template>
  <common-r-dialog
    v-if="platform"
    v-model="show"
    icon="mdi-delete"
    scroll-content
    :width="lgAndUp ? '50vw' : '95vw'"
    @close="closeDialog"
  >
    <template #content>
      <v-row
        class="justify-center align-center pa-2"
        no-gutters
      >
        <span class="mr-1">Removing platform</span>
        <common-platform-icon :slug="platform.slug" />
        <span class="ml-1">{{ platform.name }} - [<span class="text-romm-accent-1">{{
          platform.fs_slug
        }}</span>] from RomM.</span>
        <span class="ml-1">Do you confirm?</span>
      </v-row>
    </template>
    <template #append>
      <v-row
        class="justify-center pa-2"
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
            @click="deletePlatform"
          >
            Confirm
          </v-btn>
        </v-btn-group>
      </v-row>
    </template>
  </common-r-dialog>
</template>

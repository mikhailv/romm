<script setup lang="ts">
import collectionApi from "@/services/api/collection";
import platformApi from "@/services/api/platform";
import userApi from "@/services/api/user";
import storeAuth from "@/stores/auth";
import storeCollections from "@/stores/collections";
import storeNavigation from "@/stores/navigation";
import storePlatforms from "@/stores/platforms";
import { onBeforeMount } from "vue";
import { useDisplay } from "vuetify";

// Props
const { smAndDown } = useDisplay();
const navigationStore = storeNavigation();
const auth = storeAuth();
const platformsStore = storePlatforms();
const collectionsStore = storeCollections();
const emitter = useNuxtApp().$emitter;
emitter?.on("refreshDrawer", async () => {
  const { data: platformData } = await platformApi.getPlatforms();
  platformsStore.set(platformData);
});

// Functions
onBeforeMount(async () => {
  await platformApi
    .getPlatforms()
    .then(({ data: platforms }) => {
      platformsStore.set(platforms);
    })
    .catch((error) => {
      console.error(error);
    });
  await collectionApi
    .getCollections()
    .then(({ data: collections }) => {
      collectionsStore.set(collections);
      collectionsStore.setFavCollection(
        collections.find(
          (collection) => collection.name.toLowerCase() === "favourites"
        )
      );
    })
    .catch((error) => {
      console.error(error);
    });
  await userApi
    .fetchCurrentUser()
    .then(({ data: user }) => {
      auth.setUser(user);
    })
    .catch((error) => {
      console.error(error);
    });
  navigationStore.resetDrawers();
});
</script>

<template>
  <navigation-main-drawer v-if="!smAndDown" />
  <navigation-main-app-bar v-if="smAndDown" />
  <navigation-platforms-drawer />
  <navigation-collections-drawer />
  <navigation-settings-drawer />
  <common-new-version />

  <slot />

  <common-platform-dialog-delete-platform />
  <common-collection-dialog-create-collection />
  <common-collection-dialog-edit-collection />
  <common-collection-dialog-add-roms />
  <common-collection-dialog-remove-roms />
  <common-collection-dialog-delete-collection />
  <common-game-dialog-search-rom />
  <common-game-dialog-match-rom />
  <common-game-dialog-copy-download-link />
  <common-game-dialog-upload-rom />
  <common-game-dialog-edit-rom />
  <common-game-dialog-delete-rom />
  <common-game-dialog-asset-delete />
  <common-search-cover />
  <management-dialog-create-platform-binding />
  <management-dialog-delete-platform-binding />
  <management-dialog-create-platform-version />
  <management-dialog-delete-platform-version />
  <management-dialog-create-exclusion />
  <administration-users-dialog-create-user />
  <administration-users-dialog-edit-user />
  <administration-users-dialog-delete-user />
  <common-loading-view />
</template>

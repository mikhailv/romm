<script setup lang="ts">
import storeAuth from "@/stores/auth";
import storeConfig from "@/stores/config";
import { storeToRefs } from "pinia";
import { ref } from "vue";

// Props
const emitter = useNuxtApp().$emitter;
const authStore = storeAuth();
const configStore = storeConfig();
const { config } = storeToRefs(configStore);
const editable = ref(false);
</script>

<template>
  <common-r-section
    icon="mdi-gamepad-variant"
    title="Platforms Versions"
  >
    <template #toolbar-append>
      <v-btn
        v-if="authStore.scopes.includes('platforms.write')"
        class="ma-2"
        rounded="0"
        size="small"
        :color="editable ? 'romm-accent-1' : ''"
        variant="text"
        icon="mdi-cog"
        @click="editable = !editable"
      />
    </template>
    <template #content>
      <v-row
        no-gutters
        class="align-center"
      >
        <v-col
          v-for="(slug, fsSlug) in config.PLATFORMS_VERSIONS"
          :key="slug"
          cols="6"
          sm="4"
          md="3"
          lg="2"
          :title="slug"
        >
          <management-platform-bind-card
            :editable="authStore.scopes.includes('platforms.write') && editable"
            :slug="slug"
            :fs-slug="fsSlug"
            @click-edit="
              emitter?.emit('showCreatePlatformVersionDialog', {
                fsSlug: fsSlug,
                slug: slug,
              })
            "
            @click-delete="
              emitter?.emit('showDeletePlatformVersionDialog', {
                fsSlug: fsSlug,
                slug: slug,
              })
            "
          />
        </v-col>
        <v-col
          cols="6"
          sm="4"
          md="3"
          lg="2"
          class="px-1"
        >
          <management-add-btn
            :enabled="editable"
            @click="
              emitter?.emit('showCreatePlatformVersionDialog', {
                fsSlug: '',
                slug: '',
              })
            "
          />
        </v-col>
      </v-row>
    </template>
  </common-r-section>
</template>

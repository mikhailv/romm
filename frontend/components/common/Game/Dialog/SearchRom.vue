<script setup lang="ts">
import romApi from "@/services/api/rom";
import type { SimpleRom } from "@/stores/roms";
import { onBeforeUnmount, ref } from "vue";
import { useDisplay } from "vuetify";

// Define types
type Platform = {
  platform_name: string;
  platform_slug: string;
};

type SelectItem = {
  raw: Platform;
};

// Props
const { lgAndUp } = useDisplay();
const show = ref(false);
const searching = ref(false);
const searched = ref(false);
const router = useRouter();
const searchedRoms = ref<Platform[]>([]);
const filteredRoms = ref<SimpleRom[]>([]);
const platforms = ref<Platform[]>([]);
const selectedPlatform = ref<Platform | null>(null);
const searchValue = ref("");
const emitter = useNuxtApp().$emitter;
emitter?.on("showSearchRomDialog", () => {
  show.value = true;
});

// Functions
async function filterRoms() {
  if (!selectedPlatform.value) {
    filteredRoms.value = searchedRoms.value as SimpleRom[];
  } else {
    filteredRoms.value = searchedRoms.value.filter(
      (rom: { platform_name: string }) =>
        rom.platform_name == selectedPlatform.value?.platform_name
    ) as SimpleRom[];
  }
}

function clearFilter() {
  selectedPlatform.value = null;
  filterRoms();
}

async function searchRoms() {
  if (searchValue.value != "") {
    // Auto hide android keyboard
    const inputElement = document.getElementById("search-text-field");
    inputElement?.blur();
    searching.value = true;
    searched.value = true;
    searchedRoms.value = (
      await romApi.getRoms({ searchTerm: searchValue.value })
    ).data.sort((a, b) => {
      return a.platform_name.localeCompare(b.platform_name);
    });
    platforms.value = [
      ...new Map(
        searchedRoms.value.map((rom): [string, Platform] => [
          rom.platform_name,
          {
            platform_name: rom.platform_name,
            platform_slug: rom.platform_slug,
          },
        ])
      ).values(),
    ];
    filterRoms();
    searching.value = false;
  }
}

function onGameClick(emitData: { rom: SimpleRom; event: MouseEvent }) {
  router.push({ name: "rom-id", params: { id: emitData.rom.id } });
  closeDialog();
}

function closeDialog() {
  show.value = false;
  searched.value = false;
}

onBeforeUnmount(() => {
  emitter?.off("showSearchRomDialog");
});
</script>

<template>
  <common-r-dialog
    v-model="show"
    icon="mdi-magnify"
    :loading-condition="searching"
    :empty-state-condition="searchedRoms?.length == 0 && searched"
    empty-state-type="game"
    scroll-content
    :width="lgAndUp ? '60vw' : '95vw'"
    :height="lgAndUp ? '90vh' : '775px'"
  >
    <template #toolbar>
      <v-row
        class="align-center"
        no-gutters
      >
        <v-col
          cols="5"
          md="6"
          lg="7"
        >
          <v-text-field
            id="search-text-field"
            v-model="searchValue"
            autofocus
            :disabled="searching"
            label="Search"
            hide-details
            class="bg-terciary"
            @keyup.enter="searchRoms"
            @click:clear="searchRoms"
          />
        </v-col>
        <v-col
          cols="5"
          lg="4"
        >
          <v-select
            v-model="selectedPlatform"
            label="Platform"
            class="bg-terciary"
            item-title="platform_name"
            :disabled="platforms.length == 0 || searching"
            hide-details
            clearable
            single-line
            return-object
            :items="platforms"
            @click:clear="clearFilter"
            @update:model-value="filterRoms"
          >
            <template #item="{ props, item }">
              <v-list-item
                class="py-2"
                v-bind="props"
                :title="(item as SelectItem).raw.platform_name ?? ''"
              >
                <template #prepend>
                  <common-platform-icon
                    :key="(item as SelectItem).raw.platform_slug"
                    :size="35"
                    :slug="(item as SelectItem).raw.platform_slug"
                  />
                </template>
              </v-list-item>
            </template>
            <template #selection="{ item }">
              <v-list-item
                class="px-0"
                :title="(item as SelectItem).raw.platform_name ?? ''"
              >
                <template #prepend>
                  <common-platform-icon
                    :key="(item as SelectItem).raw.platform_slug"
                    :size="35"
                    :slug="(item as SelectItem).raw.platform_slug"
                  />
                </template>
              </v-list-item>
            </template>
          </v-select>
        </v-col>
        <v-col>
          <v-btn
            type="submit"
            class="bg-terciary"
            rounded="0"
            variant="text"
            icon="mdi-magnify"
            block
            :disabled="searching"
            @click="searchRoms"
          />
        </v-col>
      </v-row>
    </template>
    <template #content>
      <v-row no-gutters>
        <v-col
          v-for="rom in filteredRoms"
          v-show="!searching"
          class="pa-1"
          cols="4"
          sm="3"
          md="2"
        >
          <common-game-card
            :rom="rom"
            title-on-hover
            show-flags
            transform-scale
            show-common-platform-icon
            show-fav
            @click="onGameClick({ rom, event: $event })"
          />
        </v-col>
      </v-row>
    </template>
  </common-r-dialog>
</template>

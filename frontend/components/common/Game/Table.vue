<script setup lang="ts">
import romApi from "@/services/api/rom";
import storeDownload from "@/stores/download";
import storeRoms, { type SimpleRom } from "@/stores/roms";
import {
  formatBytes,
  isEmulationSupported,
  languageToEmoji,
  regionToEmoji,
} from "@/utils";
import { isNull } from "lodash";
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useDisplay } from "vuetify";

// Props
const { xs } = useDisplay();
const emitter = useNuxtApp().$emitter;
emitter?.on("updateDataTablePages", updateDataTablePages);
const showSiblings = isNull(localStorage.getItem("settings.showSiblings"))
  ? true
  : localStorage.getItem("settings.showSiblings") === "true";
const router = useRouter();
const route = useRoute();
const downloadStore = storeDownload();
const romsStore = storeRoms();
const page = ref(parseInt(window.location.hash.slice(1)) || 1);
const storedRomsPerPage = parseInt(localStorage.getItem("romsPerPage") ?? "");
const itemsPerPage = ref(isNaN(storedRomsPerPage) ? 25 : storedRomsPerPage);
const pageCount = ref(0);
const PER_PAGE_OPTIONS = [10, 25, 50, 100];
const HEADERS = [
  {
    title: "Title",
    align: "start",
    sortable: true,
    key: "name",
  },
  {
    title: "",
    align: "start",
    sortable: false,
    key: "is_fav",
  },
  {
    title: "Size",
    align: "start",
    sortable: true,
    key: "file_size_bytes",
  },
  {
    title: "Reg",
    align: "start",
    sortable: true,
    key: "regions",
  },
  {
    title: "Lang",
    align: "start",
    sortable: true,
    key: "languages",
  },
  {
    title: "Rev",
    align: "start",
    sortable: true,
    key: "revision",
  },
  { title: "", align: "end", key: "actions", sortable: false },
] as const;

// Functions
function rowClick(_: Event, row: { item: SimpleRom }) {
  router.push({ name: "rom-id", params: { id: row.item.id } });
}

function updateDataTablePages() {
  pageCount.value = Math.ceil(
    romsStore.filteredRoms.length / itemsPerPage.value
  );
}

function updateUrlHash() {
  window.location.hash = String(page.value);
}

watch(itemsPerPage, async () => {
  localStorage.setItem("romsPerPage", itemsPerPage.value.toString());
  updateDataTablePages();
});

// Watch route to avoid race condition
watch(route, () => {
  page.value = parseInt(window.location.hash.slice(1)) || 1;
});

onMounted(() => {
  updateDataTablePages();
});
</script>

<template>
  <v-data-table
    v-model="romsStore._selectedIDs"
    v-model:page="page"
    :items-per-page="itemsPerPage"
    :items-per-page-options="PER_PAGE_OPTIONS"
    :item-value="(item) => item.id"
    :items="romsStore.filteredRoms"
    :headers="HEADERS"
    show-select
    fixed-header
    fixed-footer
    hide-default-footer
    hover
    @click:row="rowClick"
  >
    <template #item.name="{ item }">
      <td class="name-row">
        <v-list-item class="px-0">
          <template #prepend>
            <common-game-r-avatar :rom="item" />
          </template>
          <v-row no-gutters>
            <v-col>{{ item.name }}</v-col>
          </v-row>
          <v-row no-gutters>
            <v-col class="text-romm-accent-1">
              {{
                item.file_name
              }}
            </v-col>
          </v-row>
          <template #append>
            <v-chip
              v-if="item.siblings && item.siblings.length > 0 && showSiblings"
              class="translucent-dark ml-2"
              size="x-small"
            >
              <span class="text-caption">+{{ item.siblings.length }}</span>
            </v-chip>
          </template>
        </v-list-item>
      </td>
    </template>
    <template #item.is_fav="{ item }">
      <common-game-fav-btn :rom="item" />
    </template>
    <template #item.file_size_bytes="{ item }">
      <v-chip
        size="x-small"
        label
      >
        {{
          formatBytes(item.file_size_bytes)
        }}
      </v-chip>
    </template>
    <template #item.regions="{ item }">
      <span
        v-for="region in item.regions"
        class="px-1"
      >
        {{ regionToEmoji(region) }}
      </span>
    </template>
    <template #item.languages="{ item }">
      <span
        v-for="language in item.languages"
        class="px-1"
      >
        {{ languageToEmoji(language) }}
      </span>
    </template>
    <template #item.actions="{ item }">
      <v-btn-group
        divided
        density="compact"
      >
        <v-btn
          :disabled="downloadStore.value.includes(item.id)"
          download
          size="small"
          @click.stop="romApi.downloadRom({ rom: item })"
        >
          <v-icon>mdi-download</v-icon>
        </v-btn>
        <v-btn
          v-if="isEmulationSupported(item.platform_slug)"
          size="small"
          @click.stop="
            $router.push({
              name: 'play-id',
              params: { id: item?.id },
            })
          "
        >
          <v-icon>mdi-play</v-icon>
        </v-btn>
        <v-menu location="bottom">
          <template #activator="{ props }">
            <v-btn
              v-bind="props"
              size="small"
            >
              <v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
          </template>
          <common-game-admin-menu :rom="item" />
        </v-menu>
      </v-btn-group>
    </template>

    <template #bottom>
      <v-divider />
      <div>
        <v-row
          no-gutters
          class="pa-1 align-center justify-center"
        >
          <v-col
            cols="8"
            sm="9"
            md="10"
            class="px-3"
          >
            <v-pagination
              v-model="page"
              :show-first-last-page="!xs"
              rounded="0"
              active-color="romm-accent-1"
              :length="pageCount"
              @update:model-value="updateUrlHash"
            />
          </v-col>
          <v-col>
            <v-select
              v-model="itemsPerPage"
              class="pa-2"
              label="Roms per page"
              density="compact"
              variant="outlined"
              :items="PER_PAGE_OPTIONS"
              hide-details
            />
          </v-col>
        </v-row>
      </div>
    </template>
  </v-data-table>
</template>
<style scoped>
.name-row {
  min-width: 350px;
}
</style>

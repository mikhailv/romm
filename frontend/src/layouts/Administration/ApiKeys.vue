<script setup lang="ts">
import Task from "@/components/Settings/TaskOption.vue";
import RSection from "@/components/common/RSection.vue";
import api from "@/services/api/index";
import storeHeartbeat from "@/stores/heartbeat";
import storeRunningTasks from "@/stores/runningTasks";
import type { Events } from "@/types/emitter";
import { convertCronExperssion } from "@/utils";
import type { Emitter } from "mitt";
import { computed, inject } from "vue";
import { useDisplay } from "vuetify";

// Props
const emitter = inject<Emitter<Events>>("emitter");
const { smAndDown } = useDisplay();
const heartbeatStore = storeHeartbeat();
const runningTasks = storeRunningTasks();

const tasks = computed(() => [
  {
    title: heartbeatStore.value.WATCHER.TITLE,
    description: heartbeatStore.value.WATCHER.MESSAGE,
    icon: heartbeatStore.value.WATCHER.ENABLED
      ? "mdi-file-check-outline"
      : "mdi-file-remove-outline",
    enabled: heartbeatStore.value.WATCHER.ENABLED,
  },
  {
    title: heartbeatStore.value.SCHEDULER.RESCAN.TITLE,
    description:
      heartbeatStore.value.SCHEDULER.RESCAN.MESSAGE +
      " " +
      convertCronExperssion(heartbeatStore.value.SCHEDULER.RESCAN.CRON),
    icon: heartbeatStore.value.SCHEDULER.RESCAN.ENABLED
      ? "mdi-clock-check-outline"
      : "mdi-clock-remove-outline",
    enabled: heartbeatStore.value.SCHEDULER.RESCAN.ENABLED,
  },
  {
    title: heartbeatStore.value.SCHEDULER.SWITCH_TITLEDB.TITLE,
    description:
      heartbeatStore.value.SCHEDULER.SWITCH_TITLEDB.MESSAGE +
      " " +
      convertCronExperssion(heartbeatStore.value.SCHEDULER.SWITCH_TITLEDB.CRON),
    icon: heartbeatStore.value.SCHEDULER.SWITCH_TITLEDB.ENABLED
      ? "mdi-clock-check-outline"
      : "mdi-clock-remove-outline",
    enabled: heartbeatStore.value.SCHEDULER.SWITCH_TITLEDB.ENABLED,
  },
]);

// Methods
const runAllTasks = async () => {
  runningTasks.value = true;
  const result = await api.post("/tasks/run");
  runningTasks.value = false;
  if (result.status !== 200) {
    return emitter?.emit("snackbarShow", {
      msg: "Error running tasks",
      icon: "mdi-close-circle",
      color: "red",
    });
  }

  emitter?.emit("snackbarShow", {
    msg: result.data.msg,
    icon: "mdi-check-circle",
    color: "green",
  });
};
</script>
<template>
  <r-section icon="mdi-key" title="API Keys">
    <template #content>
      <v-row no-gutters class="align-center">
        <v-col cols="12">
          <v-expansion-panels flat multiple>
            <v-expansion-panel class="bg-terciary">
              <template #title>
                <v-avatar class="mr-1" size="30" rounded="1">
                  <v-img src="/assets/scrappers/igdb.png"
                /></v-avatar>
                <span class="ml-2">IGDB</span>
              </template>
              <template #text>
                <v-row no-gutters>
                  <v-col cols="12" md="6">
                    <v-text-field
                      label="Client ID"
                      hide-details
                      variant="outlined"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-text-field
                      label="Client Secret"
                      hide-details
                      variant="outlined"
                      :class="{ 'mt-2': smAndDown, 'ml-2': !smAndDown }"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </template>
            </v-expansion-panel>

            <v-expansion-panel class="bg-terciary">
              <template #title>
                <v-avatar class="mr-1" size="30" rounded="1">
                  <v-img src="/assets/scrappers/moby.png"
                /></v-avatar>
                <span class="ml-2">Mobygames</span>
              </template>
              <template #text>
                <v-row no-gutters>
                  <v-col>
                    <v-text-field
                      label="API Key"
                      hide-details
                      variant="outlined"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </template>
            </v-expansion-panel>

            <v-expansion-panel class="bg-terciary">
              <template #title>
                <v-avatar class="mr-1" size="30" rounded="1">
                  <v-img src="/assets/scrappers/sgdb.png"
                /></v-avatar>
                <span class="ml-2">SteamgridDB</span>
              </template>
              <template #text>
                <v-row no-gutters>
                  <v-col>
                    <v-text-field
                      label="API Key"
                      hide-details
                      variant="outlined"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </template>
            </v-expansion-panel>
          </v-expansion-panels>
        </v-col>
      </v-row>
    </template>
  </r-section>
</template>

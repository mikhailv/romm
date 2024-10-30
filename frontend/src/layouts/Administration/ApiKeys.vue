<script setup lang="ts">
import Task from "@/components/Settings/TaskOption.vue";
import RSection from "@/components/common/RSection.vue";
import api from "@/services/api/index";
import storeHeartbeat from "@/stores/heartbeat";
import storeRunningTasks from "@/stores/runningTasks";
import type { Events } from "@/types/emitter";
import { convertCronExperssion } from "@/utils";
import type { Emitter } from "mitt";
import { computed, inject, ref } from "vue";
import { useDisplay } from "vuetify";

// Props
const emitter = inject<Emitter<Events>>("emitter");
const { smAndDown } = useDisplay();
const heartbeatStore = storeHeartbeat();
const runningTasks = storeRunningTasks();
const visibleIGDBId = ref(false);
const visibleIGDBSecret = ref(false);
const visibleMobyKey = ref(false);
const visibleSGDBKey = ref(false);

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
      <v-row no-gutters class="pa-2 align-center">
        <v-col cols="12" md="6">
          <v-text-field
            label="Client ID"
            hide-details
            variant="outlined"
            :append-inner-icon="visibleIGDBId ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="visibleIGDBId = !visibleIGDBId"
            :type="visibleIGDBId ? 'text' : 'password'"
            ><template #prepend-inner
              ><v-avatar size="30" rounded="1">
                <v-img src="/assets/scrappers/igdb.png"
              /></v-avatar>
              <span class="ml-2 mr-4 text-grey text-caption"
                >IGDB</span
              ></template
            ></v-text-field
          >
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            label="Client Secret"
            hide-details
            variant="outlined"
            :class="{ 'mt-2': smAndDown, 'ml-2': !smAndDown }"
            :append-inner-icon="visibleIGDBSecret ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="visibleIGDBSecret = !visibleIGDBSecret"
            :type="visibleIGDBSecret ? 'text' : 'password'"
          >
            <template #prepend-inner
              ><v-avatar size="30" rounded="1">
                <v-img src="/assets/scrappers/igdb.png"
              /></v-avatar>
              <span class="ml-2 mr-4 text-grey text-caption"
                >IGDB</span
              ></template
            >
          </v-text-field>
        </v-col>
      </v-row>

      <v-row no-gutters class="pa-2">
        <v-col>
          <v-text-field
            label="API Key"
            hide-details
            variant="outlined"
            :append-inner-icon="visibleMobyKey ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="visibleMobyKey = !visibleMobyKey"
            :type="visibleMobyKey ? 'text' : 'password'"
            ><template #prepend-inner
              ><v-avatar size="30" rounded="1">
                <v-img src="/assets/scrappers/moby.png"
              /></v-avatar>
              <span class="ml-2 mr-4 text-grey text-caption"
                >Mobygames</span
              ></template
            ></v-text-field
          >
        </v-col>
      </v-row>

      <v-row no-gutters class="pa-2">
        <v-col>
          <v-text-field
            label="API Key"
            hide-details
            variant="outlined"
            :append-inner-icon="visibleSGDBKey ? 'mdi-eye-off' : 'mdi-eye'"
            @click:append-inner="visibleSGDBKey = !visibleSGDBKey"
            :type="visibleSGDBKey ? 'text' : 'password'"
            ><template #prepend-inner
              ><v-avatar size="30" rounded="1">
                <v-img src="/assets/scrappers/sgdb.png"
              /></v-avatar>
              <span class="ml-2 mr-4 text-grey text-caption"
                >SteamgridDB</span
              ></template
            ></v-text-field
          >
        </v-col>
      </v-row>
    </template>
  </r-section>
</template>

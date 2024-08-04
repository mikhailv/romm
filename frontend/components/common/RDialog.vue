<script setup lang="ts">
import { onMounted, ref, useSlots } from "vue";

// Props
withDefaults(
  defineProps<{
    modelValue: boolean;
    loadingCondition?: boolean;
    emptyStateCondition?: boolean;
    emptyStateType?: string | null;
    expandContentOnEmptyState?: boolean;
    scrollContent?: boolean;
    showRommIcon?: boolean;
    icon?: string | null;
    width?: string;
    height?: string;
  }>(),
  {
    loadingCondition: false,
    emptyStateCondition: false,
    emptyStateType: null,
    expandContentOnEmptyState: false,
    scrollContent: false,
    showRommIcon: false,
    icon: null,
    width: "",
    height: "",
  }
);
const emit = defineEmits(["update:modelValue", "close"]);
const hasToolbarSlot = ref(false);
const hasPrependSlot = ref(false);
const hasAppendSlot = ref(false);
const hasFooterSlot = ref(false);

// Functions
function closeDialog() {
  emit("update:modelValue", false);
  emit("close");
}

onMounted(() => {
  const slots = useSlots();
  hasToolbarSlot.value = !!slots.toolbar;
  hasPrependSlot.value = !!slots.prepend;
  hasAppendSlot.value = !!slots.append;
  hasFooterSlot.value = !!slots.footer;
});
</script>

<template>
  <v-dialog
    :model-value="modelValue"
    :scrim="true"
    :width="width"
    scroll-strategy="block"
    no-click-animation
    persistent
    @click:outside="closeDialog"
    @keydown.esc="closeDialog"
  >
    <v-card
      rounded="0"
      :height="height"
    >
      <v-toolbar
        density="compact"
        class="bg-terciary"
      >
        <v-icon
          v-if="icon"
          :icon="icon"
          class="ml-5"
        />
        <common-romm-iso
          v-if="showRommIcon"
          :size="30"
          class="mx-4"
        />
        <slot name="header" />
        <template #append>
          <v-btn
            rounded="0"
            variant="text"
            icon="mdi-close"
            @click="closeDialog"
          />
        </template>
      </v-toolbar>

      <v-divider />

      <v-toolbar
        v-if="hasToolbarSlot"
        density="compact"
        class="bg-terciary"
      >
        <slot name="toolbar" />
      </v-toolbar>
      <v-divider />

      <v-card-text
        v-if="hasPrependSlot"
        class="pa-1"
      >
        <slot name="prepend" />
      </v-card-text>

      <v-card-text
        id="common-r-dialog-content"
        class="pa-1"
        :class="{ scroll: scrollContent }"
      >
        <v-row
          v-if="loadingCondition"
          class="justify-center align-center h-100"
          no-gutters
        >
          <v-progress-circular
            :width="2"
            :size="40"
            color="romm-accent-1"
            indeterminate
          />
        </v-row>

        <v-row
          v-if="!loadingCondition && emptyStateCondition"
          class="justify-center align-center h-100"
          no-gutters
        >
          <common-empty-game v-if="emptyStateType == 'game'" />
          <common-empty-platform v-else-if="emptyStateType == 'platform'" />
          <common-empty-firmware v-else-if="emptyStateType == 'firmware'" />
          <slot
            v-else
            name="emptyState"
          />
        </v-row>

        <slot name="content" />
      </v-card-text>
      <v-card-text
        v-if="hasAppendSlot"
        class="pa-1"
      >
        <slot name="append" />
      </v-card-text>

      <template v-if="hasFooterSlot">
        <v-divider />
        <v-toolbar
          class="bg-terciary"
          density="compact"
        >
          <slot name="footer" />
        </v-toolbar>
      </template>
    </v-card>
  </v-dialog>
</template>

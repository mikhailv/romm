<script setup lang="ts">
import { isKeyof } from "@/types";
import { autoThemeKey, themes } from "assets/styles/themes";
import { computed, ref } from "vue";
import { useTheme } from "vuetify";

// Props
const theme = useTheme();
const storedTheme = parseInt(localStorage.getItem("settings.theme") ?? "");
const selectedTheme = ref(isNaN(storedTheme) ? autoThemeKey : storedTheme);
const themeOptions = computed(() => [
  {
    name: "dark",
    icon: "mdi-moon-waning-crescent",
  },
  {
    name: "light",
    icon: "mdi-white-balance-sunny",
  },
  {
    name: "auto",
    icon: "mdi-theme-light-dark",
  },
]);

// Functions
function toggleTheme() {
  localStorage.setItem("settings.theme", selectedTheme.value.toString());
  const mediaMatch = window.matchMedia("(prefers-color-scheme: dark)");
  if (selectedTheme.value === autoThemeKey) {
    theme.global.name.value = mediaMatch.matches ? "dark" : "light";
  } else if (isKeyof(selectedTheme.value, themes)) {
    theme.global.name.value = themes[selectedTheme.value];
  }
}
</script>

<template>
  <common-r-section
    icon="mdi-brush-variant"
    title="Theme"
  >
    <template #content>
      <v-item-group
        v-model="selectedTheme"
        mandatory
        @update:model-value="toggleTheme"
      >
        <v-row no-gutters>
          <v-col
            v-for="theme in themeOptions"
            cols="4"
            sm="3"
            md="2"
            class="pa-2"
          >
            <settings-theme-option
              :key="theme.name"
              :text="theme.name"
              :icon="theme.icon"
            />
          </v-col>
        </v-row>
      </v-item-group>
    </template>
  </common-r-section>
</template>

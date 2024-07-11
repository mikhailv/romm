import { createVuetify } from "vuetify";
import { themes, dark, light, autoThemeKey } from "assets/styles/themes";
import { isKeyof } from "@/types";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import "vuetify/styles";
import "@mdi/font/css/materialdesignicons.css";

export default defineNuxtPlugin((nuxtApp) => {
  // Check if running on the client side
  const mediaMatch = window.matchMedia("(prefers-color-scheme: dark)");
  mediaMatch.addEventListener("change", (event) => {
    instance.theme.global.name.value = event.matches ? "dark" : "light";
  });

  function getTheme() {
    const storedTheme = parseInt(localStorage.getItem("settings.theme") ?? "");

    if (
      !isNaN(storedTheme) &&
      storedTheme !== autoThemeKey &&
      isKeyof(storedTheme, themes)
    ) {
      return themes[storedTheme];
    }

    return mediaMatch.matches ? "dark" : "light";
  }

  const vuetify = createVuetify({
    components,
    directives,
    icons: {
      defaultSet: "mdi",
    },
    theme: {
      defaultTheme: getTheme(),
      themes: {
        dark,
        light,
      },
    },
  });

  nuxtApp.vueApp.use(vuetify);
});

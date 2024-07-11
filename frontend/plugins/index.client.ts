import { defineNuxtPlugin } from "#app";
import { App } from "vue";
import vuetify from "@/plugins/vuetify.client";
import pinia from "@/plugins/pinia.client";
import { loadFonts } from "@/plugins/webfontloader.client";

export default defineNuxtPlugin((nuxtApp) => {
  const registerPlugins = (app: App<Element>) => {
    loadFonts();
  };

  // Ensure plugins are registered on client side
  registerPlugins(nuxtApp.vueApp);
});

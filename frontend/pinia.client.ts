import { defineNuxtPlugin } from "#app";
import { createPinia } from "pinia";
import { markRaw } from "vue";

export default defineNuxtPlugin((nuxtApp) => {
  const pinia = createPinia();
  const router = useRouter();

  pinia.use(({ store }) => {
    store.$router = markRaw(router);
  });

  nuxtApp.vueApp.use(pinia);
});

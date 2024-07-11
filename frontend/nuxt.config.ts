import { fileURLToPath } from "url";
import { transformAssetUrls } from "vite-plugin-vuetify";

export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  ssr: false,
  devtools: { enabled: false },
  modules: ["@pinia/nuxt"],
  css: [
    "vuetify/lib/styles/main.sass",
    "@mdi/font/css/materialdesignicons.min.css",
    "@/assets/styles/fonts.css",
    "@/assets/styles/scrollbar.css",
    "@/assets/styles/common.css",
  ],
  build: {
    target: "esnext",
    transpile: ["vuetify"],
  },
  plugins: [
    "~/plugins/api.client.ts",
    "~/plugins/emitter.client.ts",
    "~/plugins/vuetify.client.ts",
    "~/plugins/webfontloader.client.ts",
  ],
  define: {
    "process.env": {},
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: true,
  },
  alias: {
    "@": fileURLToPath(new URL(".", import.meta.url)),
  },
  nitro: {
    devProxy: {
      "/api": {
        target:
          "http://127.0.0.1:" + (process.env.VITE_BACKEND_DEV_PORT || "5000"),
        changeOrigin: false,
        rewrite: (path: string) => path.replace(/^\/api/, ""),
      },
      "/ws": {
        target:
          "http://127.0.0.1:" + (process.env.VITE_BACKEND_DEV_PORT || "5000"),
        changeOrigin: false,
        ws: true,
      },
      "/openapi.json": {
        target:
          "http://127.0.0.1:" + (process.env.VITE_BACKEND_DEV_PORT || "5000"),
        changeOrigin: false,
        rewrite: (path: string) =>
          path.replace(/^\/openapi.json/, "/openapi.json"),
      },
    },
  },
  server: {
    port: 3000,
  },
  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
});

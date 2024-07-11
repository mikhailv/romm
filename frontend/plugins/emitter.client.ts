import mitt from "mitt";
import type { Events } from "@/types/emitter";

export default defineNuxtPlugin((nuxtApp) => {
  const emitter = mitt<Events>();
  nuxtApp.provide("emitter", emitter);
});

import type { Events } from "@/types/emitter";
import mitt from "mitt";

export default defineNuxtPlugin((nuxtApp) => {
  const emitter = mitt<Events>();
  nuxtApp.provide("emitter", emitter);
});

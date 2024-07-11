import type { Emitter } from "mitt";
import type { Events } from "@/types/emitter";

declare module "#app" {
  interface NuxtApp {
    $emitter: Emitter<Events>;
  }
}

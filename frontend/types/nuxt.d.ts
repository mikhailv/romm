declare module "#app" {
  interface NuxtApp {
    $emitter: Emitter<Events>;
  }
}

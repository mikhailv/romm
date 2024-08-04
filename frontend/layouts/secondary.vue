<script setup lang="ts">
import storeHeartbeat from "@/stores/heartbeat";

// Props
const heartbeat = storeHeartbeat();
</script>
<template>
  <span id="bg" />

  <slot />

  <div
    id="version"
    class="position-absolute"
  >
    <span class="text-white">{{ heartbeat.value.VERSION }}</span>
  </div>
</template>

<style>
#bg {
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  position: absolute;
  background: url("/images/login_bg.png") center center;
  background-size: cover;
}
#version {
  text-shadow: 1px 1px 1px #000000, 0 0 1px #000000;
  bottom: 0.3rem;
  right: 0.5rem;
}
</style>

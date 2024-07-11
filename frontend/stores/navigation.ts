import { defineStore } from "pinia";

export default defineStore("navigation", {
  state: () => ({
    activePlatformsDrawer: false,
    activeCollectionsDrawer: false,
    activeSettingsDrawer: false,
  }),

  actions: {
    switchActivePlatformsDrawer() {
      this.activeCollectionsDrawer = false;
      this.activeSettingsDrawer = false;
      this.activePlatformsDrawer = !this.activePlatformsDrawer;
    },
    switchActiveCollectionsDrawer() {
      this.activePlatformsDrawer = false;
      this.activeSettingsDrawer = false;
      this.activeCollectionsDrawer = !this.activeCollectionsDrawer;
    },
    switchActiveSettingsDrawer() {
      this.activePlatformsDrawer = false;
      this.activeCollectionsDrawer = false;
      this.activeSettingsDrawer = !this.activeSettingsDrawer;
    },
    goHome() {
      this.resetDrawers();
      const router = useRouter();
      router.push({ name: "index" });
    },
    goScan() {
      this.resetDrawers();
      const router = useRouter();
      router.push("/scan");
    },
    resetDrawers() {
      this.activePlatformsDrawer = false;
      this.activeCollectionsDrawer = false;
      this.activeSettingsDrawer = false;
    },
  },
});

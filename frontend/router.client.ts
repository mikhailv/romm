// Composables
import { createRouter, createWebHistory } from "vue-router";
import storeHeartbeat from "@/stores/heartbeat";

const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import("@/pages/Login.vue"),
  },
  {
    path: "/setup",
    name: "setup",
    component: () => import("@/pages/Setup.vue"),
  },
  {
    path: "/",
    name: "home",
    component: () => import("@/pages/Home.vue"),
    children: [
      {
        path: "/",
        name: "dashboard",
        component: () => import("@/pages/Dashboard.vue"),
      },
      {
        path: "/platform/:platform",
        name: "platform",
        component: () => import("@/pages/Gallery/Platform.vue"),
      },
      {
        path: "/collection/:collection",
        name: "collection",
        component: () => import("@/pages/Gallery/Collection.vue"),
      },
      {
        path: "/rom/:rom",
        name: "rom",
        component: () => import("@/pages/GameDetails.vue"),
      },
      {
        path: "/rom/:rom/play",
        name: "play",
        component: () => import("@/pages/Play/Base.vue"),
      },
      {
        path: "/scan",
        name: "scan",
        component: () => import("@/pages/Scan.vue"),
      },
      {
        path: "/management",
        name: "management",
        component: () => import("@/pages/Management.vue"),
      },
      {
        path: "/settings",
        name: "settings",
        component: () => import("@/pages/Settings.vue"),
      },
      {
        path: "/administration",
        name: "administration",
        component: () => import("@/pages/Administration.vue"),
      },
      {
        path: "/:pathMatch(.*)*",
        name: "noMatch",
        component: () => import("@/pages/Dashboard.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to) => {
  const heartbeat = storeHeartbeat();
  if (to.name == "setup" && !heartbeat.value.SHOW_SETUP_WIZARD) {
    router.push({ name: "dashboard" });
  }
  // TODO: check permission for pages. Ex: view user can access to /scan view
});

router.afterEach(() => {
  // Scroll to top to avoid annoying behaviour in mobile
  window.scrollTo({ top: 0, left: 0 });
});

export default router;

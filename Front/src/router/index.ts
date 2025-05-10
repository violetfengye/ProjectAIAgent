import { createRouter, createWebHistory } from "vue-router";
import type { RouteRecordRaw } from "vue-router";

const routes: RouteRecordRaw[] = [
  {
    path: "/",
    name: "Layout",
    component: () => import("@/layouts/DefaultLayout.vue"),
    children: [
      {
        path: "",
        name: "Home",
        component: () => import("@/views/Home.vue"),
      },
      {
        path: "requirements",
        name: "Requirements",
        component: () => import("@/views/requirements/Index.vue"),
      },
      {
        path: "architecture",
        name: "Architecture",
        component: () => import("@/views/architecture/Index.vue"),
      },
      {
        path: "code",
        name: "Code",
        component: () => import("@/views/code/Index.vue"),
      },
      {
        path: "testing",
        name: "Testing",
        component: () => import("@/views/testing/Index.vue"),
      },
      {
        path: "deployment",
        name: "Deployment",
        component: () => import("@/views/deployment/Index.vue"),
      },
    ],
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/Login.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;

import { createRouter, createWebHistory } from "vue-router";
import Index from "./components/Index.vue";
import Login from "./components/Login.vue";
import Register from "./components/Register.vue";
import Home from "./components/Home.vue";

import { refreshAuthToken } from "./utils/auth";

const routes = [
  { path: "/", component: Index },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/home", component: Home, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guard to check for authentication
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const isRefreshed = await refreshAuthToken();
      if (!isRefreshed) {
        next("/login");
      } else {
        next();
      }
  }
  else {
    next();
  }
});

export default router;
import { createRouter, createWebHistory } from "vue-router";
import Index from "./components/public/Index.vue";
import Login from "./components/public/Login.vue";
import Register from "./components/public/Register.vue";
import Home from "./components/private/Home.vue";

import { refreshAuthToken } from "./utils/auth";

const routes = [
  { path: "/", component: Index },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  { path: "/home", component: Home, meta: { requiresAuth: true } },
  // { path: '/game', name: 'Game', component: Game, meta: { requiresAuth: true } },
  // { path: '/friend-list', name: 'FriendList', component: FriendList, meta: { requiresAuth: true } },
  // { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
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
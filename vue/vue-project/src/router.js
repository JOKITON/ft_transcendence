import { createRouter, createWebHistory } from "vue-router";
import Index from "./components/Index.vue";
import Login from "./components/Login.vue";
import Register from "./components/Register.vue";
import Home from "./components/Home.vue";

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
router.beforeEach((to, from, next) => {
  const loggedIn = !!localStorage.getItem('user'); // Assume you store the user info in localStorage

  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    next('/login');
  } else {
    next();
  }
});

export default router;

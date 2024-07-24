import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/public/Index.vue'
import Login from '../views/public/Login.vue'
import Register from '../views/public/Register.vue'
import Home from '../views/private/Home.vue'

import { checkAndRefreshToken } from '../utils/auth'
import { fetchAndSetCsrfToken } from '../utils/csrf'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  /*
   * este es el enrutador, funciona igual que django es muy parecido
   **/
  routes: [
    { path: '/', component: Index },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/home', component: Home, meta: { requiresAuth: true } }
    // { path: '/game', name: 'Game', component: Game, meta: { requiresAuth: true } },
    // { path: '/friend-list', name: 'FriendList', component: FriendList, meta: { requiresAuth: true } },
    // { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  ]
})

// Fetch and set CSRF token when the app starts
fetchAndSetCsrfToken()
  .then(() => {
    console.log('CSRF token set successfully')
  })
  .catch((error) => {
    console.error('Failed to fetch and set CSRF token:', error)
  })

// Navigation guard to check for authentication and CSRF token
router.beforeEach(async (to, from, next) => {
  try {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
      const isRefreshed = await checkAndRefreshToken()
      if (!isRefreshed) {
        next('/login')
        return
      }
    }

    // Ensure CSRF token is set
    try {
      await fetchAndSetCsrfToken()
    } catch (error) {
      console.error('Failed to fetch CSRF token:', error)
      // Optionally redirect or show an error page
      next('/login')
      return
    }

    next()
  } catch (error) {
    console.error('Navigation guard error:', error)
    next('/login') // Redirect to login or show an error page if there's an issue
  }
})

export default router
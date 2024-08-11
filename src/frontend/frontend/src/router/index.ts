import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/public/Index.vue'
import RegisterForm from '../components/Registerform.vue'
import Login from '../components/Login.vue'

import Pong from '../views/private/Pong/Pong.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  /*
   * este es el enrutador, funciona igual que django es muy parecido
   **/
  routes: [
    { path: '/', name: 'home', component: Index },
    { path: '/register', name: 'register', component: RegisterForm },
    { path: '/login', name: 'login', component: Login },
    { path: '/pong', name: 'game', component: Pong }
    // { path: '/friend-list', name: 'FriendList', component: FriendList, meta: { requiresAuth: true } },
    // { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  ]
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

    next()
  } catch (error) {
    console.error('Navigation guard error:', error)
    next('/login') // Redirect to login or show an error page if there's an issue
  }
})

export default router

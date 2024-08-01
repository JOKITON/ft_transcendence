import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/public/Index.vue'
import Login from '../views/public/Login.vue'
import Register from '../views/public/Register.vue'
import Home from '../views/private/Home.vue'

import { checkAndRefreshToken } from '../utils/Api/auth'
import Pong from '../views/private/Pong/Pong.vue'
import UserList from '../views/private/UserList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  /*
   * este es el enrutador, funciona igual que django es muy parecido
   **/
  routes: [
    { path: '/', component: Index },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/home', component: Home, meta: { requiresAuth: true } },
    { path: '/pong', component: Pong },
    { path: '/user-list', name: 'userList', component: UserList, meta: { requiresAuth: true } },
    // { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  ]
})

// Navigation guard to check for authentication
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

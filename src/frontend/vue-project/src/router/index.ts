import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/public/Index.vue'
import Login from '../views/public/Login.vue'
import Register from '../views/public/Register.vue'
import Home from '../views/private/Home.vue'

import { checkAndRefreshToken, refreshAuthToken } from '../utils/Api/auth'
import PongIndex from '../views/private/Pong/PongIndex.vue'
import UserList from '../views/private/UserList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  /*
   * este es el enrutador, funciona igual que django es muy parecido
   **/
  routes: [
    { path: '/', name: 'IndexPage', component: Index },
    { path: '/register', name: 'RegisterPage', component: Register },
    { path: '/login', name: 'LoginPage', component: Login },
    { path: '/home', name: 'HomePage', component: Home, meta: { requiresAuth: true } },
    
    { path: '/pong', name: 'PongGame', component: PongIndex, meta: { requiresAuth: true } },
    { path: '/user-list', name: 'UserList', component: UserList, meta: { requiresAuth: true } },
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

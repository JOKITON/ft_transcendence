import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/public/Index.vue'
import Register from '../views/public/Register.vue'
import Login from '../views/public/Login.vue'
import Pong from '../views/private/Pong/Pong.vue'
import auth from '../services/user/services/auth/auth'
import UserList from '../views/private/UserList.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    { path: '/', name: 'home', component: Index },
    { path: '/register', name: 'register', component: Register },
    { path: '/login', name: 'login', component: Login },
    { path: '/pong', name: 'pong', component: Pong, meta: { requiresAuth: true } },
    // { path: '/user-list', name: 'UserList', component: UserList, meta: { requiresAuth: true } },
    // { path: '/friend-list', name: 'FriendList', component: FriendList, meta: { requiresAuth: true } },
    // { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  ]
})

const Auth: auth = new auth()

router.beforeEach(async (to, from, next): Promise<void> => {
  try {
    if (to.name === 'login' || to.name === 'register') {
      next()
      return
    }

    const response: boolean = await Auth.checkAndRefreshToken()
    if (to.matched.some((record) => record.meta.requiresAuth)) {
      if (response === true) {
        next()
        return
      } else {
        next('/login')
        return
      }
    }
  } catch (error) {
    console.error('Navigation guard error:', error)
    next('/login') // Redirect to login or show an error page if there's an issue
  }
})

export default router

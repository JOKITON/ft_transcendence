import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/public/Index.vue'
import RegisterForm from '../components/Registerform.vue'
import Login from '../components/Login.vue'
import Pong from '../views/private/Pong/Pong.vue'
import type { tokenResponse, token } from '@/models/auth/token'
import Api from '../utils/Api/Api'
import type ApiResponse from '../utils/Api/Api'
import { inject } from 'vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    { path: '/', name: 'home', component: Index },
    { path: '/register', name: 'register', component: RegisterForm },
    { path: '/login', name: 'login', component: Login },
    { path: '/pong', name: 'pong', component: Pong, meta: { requiresAuth: true } }
    // { path: '/friend-list', name: 'FriendList', component: FriendList, meta: { requiresAuth: true } },
    // { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
  ]
})

router.beforeEach(async (to, from, next): Promise<void> => {
  try {
    const api = inject('$api') as Api
    console.log('from to ', from, to)
    if (to.name === 'login' || to.name === 'register') {
      next()
      return
    }

    if (localStorage.getItem('token') != null) {
      api.setAccessToken(localStorage.getItem('token'))
    }

    if (to.matched.some((record) => record.meta.requiresAuth)) {
      const response: tokenResponse = await api.post<tokenResponse>(
        'token/verify',
        {
          token: localStorage.getItem('token') as string
        },
        ['status'],
        {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('token') as string}`
        }
      )
      console.log('token', response)
      if (!response || response.status !== 200) {
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

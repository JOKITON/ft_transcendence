import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/public/Index.vue'
import RegisterForm from '../components/Registerform.vue'
import Login from '../components/Login.vue'
import Pong from '../views/private/Pong/Pong.vue'
import Auth from '../services/User/Services/Auth/Auth'
import type { tokenResponse, tokenRequest } from '@/Models/User/token'
import Api from '../utils/Api/Api'
import { ref, inject } from 'vue'

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
    if (localStorage.getItem('accessToken') != null) {
      api.setAccessToken(localStorage.getItem('accessToken'))
    }
    const auth: Auth = new Auth(api)

    if (to.matched.some((record) => record.meta.requiresAuth)) {
      const token = ref<tokenRequest>({
        token: localStorage.getItem('accessToken') as string
      })
      console.log('token', token.value)
      const isRefreshed: tokenResponse = await auth.checkAndRefreshToken<tokenResponse>(token.value)
      console.log('isRefreshed', isRefreshed)
      if (isRefreshed.status != 200) {
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

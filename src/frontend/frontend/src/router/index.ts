import { createRouter, createWebHistory } from 'vue-router'
import Index from '../views/public/Index.vue'
import Register from '../views/public/Register.vue'
import Login from '../views/public/Login.vue'
import PongIndex from '../views/private/Pong/PongIndex.vue'
import auth from '../services/user/services/auth/auth'
import UserList from '../views/private/UserList.vue'
import Home from '../views/private/Home.vue'
import Profile from '../views/private/Profile.vue'
import Friends from '../views/private/Friends.vue'
import ChangePassword from '../views/private/ChangePassword.vue'
import ChangeAvatar from '../views/private/ChangeAvatar.vue'
import OtherProfile from '../views/private/OtherProfile.vue'
import UserProfile from '../views/private/UserProfile.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    { path: '/', name: 'index', component: Index },
    { path: '/register', name: 'register', component: Register },
    { path: '/login', name: 'login', component: Login },
    { path: '/home', name: 'home', component: Home, meta: { requiresAuth: true } },
    { path: '/pong', name: 'pong', component: PongIndex, meta: { requiresAuth: true } },
    { path: '/user-list', name: 'UserList', component: UserList, meta: { requiresAuth: true } },
    // { path: '/friend-list', name: 'FriendList', component: FriendList, meta: { requiresAuth: true } },
    { path: '/profile', name: 'Profile', component: Profile, meta: { requiresAuth: true } },
    { path: '/friends', name: 'Friends', component: Friends, meta: { requiresAuth: true } },
    { path: '/change-password', name: 'ChangePassword', component: ChangePassword, meta: { requiresAuth: true } },
    { path: '/change-avatar', name: 'ChangeAvatar', component: ChangeAvatar, meta: { requiresAuth: true } },
    { path: '/other-profile', name: 'OtherProfile', component: OtherProfile, meta: { requiresAuth: true } },
    { path: '/user-profile/:id', name: 'UserProfile', component: UserProfile, props: true, meta: { requiresAuth: true } },
  ]
})

const Auth: auth = new auth()

router.beforeEach(async (to, from, next): Promise<void> => {
  try {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
      const hasRefreshToken: boolean = await Auth.checkAndRefreshToken()
      if (!hasRefreshToken) {
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

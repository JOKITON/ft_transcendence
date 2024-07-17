// asthetic imports
import './assets/css/styles.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

import fetchAndSetCsrfToken from './utils/csrf'
import { setAuthHeaderFromCookie, api } from './utils/auth' // Import the functions from utils/auth.js

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)

// setup initial auth header
setAuthHeaderFromCookie()
fetchAndSetCsrfToken()

app.mount('#app')

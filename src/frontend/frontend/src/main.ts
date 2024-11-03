import './assets/css/styles.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import api from './plugins/api'
import socket from './plugins/socket'
import Chat from 'vue3-beautiful-chat'

import 'vue3-carousel/dist/carousel.css'
import './assets/css/styles.css'

const app = createApp(App)

app.use(socket)
app.use(api)
app.use(Chat)
app.use(createPinia())
app.use(router)
app.mount('#app')

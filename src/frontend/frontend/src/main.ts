import './assets/css/styles.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import api from './plugins/api'

const app = createApp(App)

app.use(api) // esto de podria hacer para tener acceso a la instancia de axios en toda la app
app.use(createPinia())
app.use(router)
app.mount('#app')

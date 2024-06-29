import { createApp } from 'vue';
import App from './App.vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import router from './router';
import "./assets/css/bootstrap.min.css";
import "./assets/css/styles.css";

const app = createApp(App);

// Set CSRF token
axios.defaults.withCredentials = true;
axios.defaults.headers.common['X-CSRFToken'] = Cookies.get('csrftoken');

// Make Axios available throughout your application
app.config.globalProperties.$axios = axios;

app.use(router);

app.mount('#app');
import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "./router";
import fetchAndSetCsrfToken from "./utils/csrf";
import "./assets/css/bootstrap.min.css";
import "./assets/css/styles.css";

const app = createApp(App);

// Set CSRF token
axios.defaults.withCredentials = true;
fetchAndSetCsrfToken();

// Set up axios to include auth token if present
const authToken = localStorage.getItem('auth_token');
if (authToken) {
  axios.defaults.headers.common['Authorization'] = `Bearer ${authToken}`;
}

app.use(router);
app.mount("#app");

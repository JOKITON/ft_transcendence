import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import Cookies from "js-cookie";
import router from "./router";
import "./assets/css/bootstrap.min.css";
import "./assets/css/styles.css";

const app = createApp(App);

// Set CSRF token
axios.defaults.withCredentials = true;

// Load CSRF token from cookie and set it in Axios defaults
const csrftoken = Cookies.get("csrftoken");
if (csrftoken) {
  axios.defaults.headers.common["X-CSRFToken"] = csrftoken;
}

// Axios request interceptor to include CSRF token
axios.interceptors.request.use(
  (config) => {
    const token = Cookies.get("csrftoken");
    if (token) {
      config.headers["X-CSRFToken"] = token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

app.use(router);
app.mount("#app");

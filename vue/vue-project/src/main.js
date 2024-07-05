import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "./router";
import fetchAndSetCsrfToken from "./utils/csrf";
import Cookies from 'js-cookie';
import "./assets/css/bootstrap.min.css";
import "./assets/css/styles.css";

const app = createApp(App);

// Set CSRF token
axios.defaults.xsrfHeaderName = 'X-CSRFToken'; // Default header for CSRF token
axios.defaults.xsrfCookieName = 'csrftoken'; // Default cookie name for CSRF token
axios.defaults.withCredentials = true;

// Update the base URL for API requests
const djangoURL = window.location.protocol + "//" + window.location.host; // Use protocol and host from the current location
axios.defaults.baseURL = djangoURL;
axios.defaults.timeout = 30000;

const api = axios.create();
export { api };

// Fetch and set CSRF token
fetchAndSetCsrfToken();

// Set up Axios to include the JWT token in the headers
const accessToken = Cookies.get('access_token');
if (accessToken) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
}

app.use(router);
app.mount("#app");

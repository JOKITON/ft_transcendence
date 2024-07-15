// main.js
import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import fetchAndSetCsrfToken from "./utils/csrf";
import { setAuthHeaderFromCookie, api } from "./utils/auth"; // Import the functions from utils/auth.js
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "./assets/css/styles.css";

// Create Vue app
const app = createApp(App);


// Initial setup
setAuthHeaderFromCookie();
fetchAndSetCsrfToken();

app.use(router);
app.mount("#app");

export { api }; // Export the api instance

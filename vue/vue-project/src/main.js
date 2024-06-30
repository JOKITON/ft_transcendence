import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";
import router from "./router";
import "./assets/css/bootstrap.min.css";
import "./assets/css/styles.css";

const app = createApp(App);

// Set CSRF token
axios.defaults.withCredentials = true;

app.use(router);
app.mount("#app");

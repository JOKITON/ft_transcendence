<template>
  <NavIndex></NavIndex>
  <div class="container">
    <div class="login-form">
      <div class="card">
        <h2 class="card-header text-center mb-4 oswald-header">Log in</h2>
        <form id="loginForm" @submit.prevent="loginUser">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              name="username"
              class="form-control"
              placeholder="Enter your username"
              required
              autofocus
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              name="password"
              class="form-control"
              placeholder="Enter your password"
              required
            />
          </div>
          <div class="d-grid gap-2">
            <button type="submit" class="btn btn-primary btn-block">
              Log in
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { api } from "../../main";
import { validateForm } from "../../utils/form";
import NavIndex from "./NavIndex.vue";

export default {
  name: "CompLogin",
  components: {
    'NavIndex': NavIndex
  },
  data() {
    return {
      form: {
        username: "",
        password: "",
      },
    };
  },
  methods: {
    async loginUser() {
      try {
        validateForm(0, this.form);

        await api.post("/api/login/", {
          username: this.form.username,
          password: this.form.password,
        });

        this.$router.push("/home");
      } catch (error) {
        console.error(
          "Login error:",
          error.response ? error.response.data : error.message
        );
        // Handle login error (e.g., show error message to user)
        alert(
          "Login failed. " +
            (error.response ? error.response.data.detail : error.message)
        );
      }
    },
  },
};
</script>

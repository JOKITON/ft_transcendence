<template>
  <header class="p-3 mb-3 border-bottom">
    <div class="container">
      <div
        class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start"
      >
        <a
          href="/"
          class="d-flex align-items-center mb-2 mb-lg-0 link-body-emphasis text-decoration-none"
        >
          <svg class="bi me-2" width="40" height="32" role="img" aria-label="Bootstrap">
            <use xlink:href="#bootstrap"></use>
          </svg>
        </a>

        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li>
            <router-link class="nav-link px-2 link-secondary" to="/overview">OverView</router-link>
          </li>
          <li><router-link class="nav-link px-2 link-secondary" to="/pong">Pong</router-link></li>
          <li>
            <router-link class="nav-link px-2 link-secondary" to="/friend-list"
              >Friend List</router-link
            >
          </li>
        </ul>

        <form class="col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3" role="search">
          <input type="search" class="form-control" placeholder="Search..." aria-label="Search" />
        </form>

        <div class="dropdown text-end">
          <p class="d-block link-body-emphasis text-decoration-none">{{ username }}</p>
          <a
            @click="toggleDropdown"
            class="d-block link-body-emphasis text-decoration-none dropdown-toggle"
          >
            <img
              src="https://avatars.githubusercontent.com/u/99480973?v=4"
              alt="mdo"
              class="rounded-circle"
              width="32"
              height="32"
            />
          </a>
          <ul class="dropdown-menu text-small" :class="{ show: isDropdownVisible }">
            <li><a @click="openSettings" class="dropdown-item">Settings</a></li>
            <li><a @click="openProfile" class="dropdown-item">Profile</a></li>
            <li>
              <hr class="dropdown-divider" />
            </li>
            <li><a @click="logoutUser" class="dropdown-item">Sign out</a></li>
          </ul>
        </div>
      </div>
    </div>
  </header>
  <main class="px-3">
    <h1>Hello, {{ username }}</h1>
    <p class="lead">
      Cover is a one-page template for building simple and beautiful home pages. Download, edit the
      text, and add your own fullscreen background photo to make it your own.
    </p>
    <p class="lead">
      <a href="#" class="btn btn-lg btn-light fw-bold border-white bg-white">Learn more</a>
    </p>
  </main>
</template>

<script>
import api from '../../utils/api'
import Cookies from 'js-cookie'

export default {
  name: 'loginHome',
  data() {
    return {
      isProfileVisible: false,
      isDropdownVisible: false,
      username: 'User' // Replace this with actual data source if necessary
    }
  },
  async created() {
    // Fetch or set the username when the component is created
    await this.fetchUsername()
  },
  methods: {
    async logoutUser() {
      try {
        const response = await api.post('logout/')
        console.log('Logout successful:', response.data)
        this.$router.push('/login')
      } catch (error) {
        console.error('Logout error:', error.response ? error.response.data : error.message)
        alert('Logout failed. ' + (error.response ? error.response.data.message : error.message))
      }
    },
    async fetchUsername() {
      try {
        const refreshToken = Cookies.get('refresh_token')
        const response = await api.get('whoami/', { refresh: refreshToken })
        this.username = response.data.username // Replace with your actual response structure
      } catch (error) {
        console.error(
          'Error fetching username:',
          error.response ? error.response.data : error.message
        )
      }
    },
    toggleDropdown() {
      this.isDropdownVisible = !this.isDropdownVisible
    },
    openSettings() {
      // Implement your settings logic here
      alert('Settings clicked')
    },
    openProfile() {
      // Implement your profile logic here
      alert('Profile clicked')
    }
  }
}
</script>

<style>
@import url('https://cdn.jsdelivr.net/npm/@docsearch/css@3');

header {
  background-color: beige;
  height: 100px;
}

main {
  background-color: #343a40;
  color: whitesmoke;
}

.bd-placeholder-img {
  font-size: 1.125rem;
  text-anchor: middle;
  -webkit-user-select: none;
  -moz-user-select: none;
  user-select: none;
}

@media (min-width: 768px) {
  .bd-placeholder-img-lg {
    font-size: 3.5rem;
  }
}

.b-example-divider {
  width: 100%;
  height: 3rem;
  background-color: rgba(0, 0, 0, 0.1);
  border: solid rgba(0, 0, 0, 0.15);
  border-width: 1px 0;
  box-shadow:
    inset 0 0.5em 1.5em rgba(0, 0, 0, 0.1),
    inset 0 0.125em 0.5em rgba(0, 0, 0, 0.15);
}

.b-example-vr {
  flex-shrink: 0;
  width: 1.5rem;
  height: 100vh;
}

.bi {
  vertical-align: -0.125em;
  fill: currentColor;
}

.nav-scroller {
  position: relative;
  z-index: 2;
  height: 2.75rem;
  overflow-y: hidden;
}

.nav-scroller .nav {
  display: flex;
  flex-wrap: nowrap;
  padding-bottom: 1rem;
  margin-top: -1px;
  overflow-x: auto;
  text-align: center;
  white-space: nowrap;
  -webkit-overflow-scrolling: touch;
}

.btn-bd-primary {
  --bd-violet-bg: #712cf9;
  --bd-violet-rgb: 112.520718, 44.062154, 249.437846;

  --bs-btn-font-weight: 600;
  --bs-btn-color: var(--bs-white);
  --bs-btn-bg: var(--bd-violet-bg);
  --bs-btn-border-color: var(--bd-violet-bg);
  --bs-btn-hover-color: var(--bs-white);
  --bs-btn-hover-bg: #6528e0;
  --bs-btn-hover-border-color: #6528e0;
  --bs-btn-focus-shadow-rgb: var(--bd-violet-rgb);
  --bs-btn-active-color: var(--bs-btn-hover-color);
  --bs-btn-active-bg: #5a23c8;
  --bs-btn-active-border-color: #5a23c8;
}

.bd-mode-toggle {
  z-index: 1500;
}

.bd-mode-toggle .dropdown-menu .active .bi {
  display: block !important;
}
</style>

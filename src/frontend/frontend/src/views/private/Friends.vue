<template>
  <NavHome></NavHome>
  <div class="row gutters-sm">
    <div class="col-sm-6 mb-3">
      <div class="card h-100 card-scrollable">
        <div class="card-body">
          <h6 class="d-flex align-items-center mb-3">Friends List</h6>
          <ul class="list-group friends-list">
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>
                <span class="status-indicator bg-success"></span>
                Jane Smith
              </span>
              <div class="btn-group">
                <button class="btn btn-primary btn-sm">Mensaje</button>
                <button class="btn btn-danger btn-sm">Bloquear</button>
                <button class="btn btn-success btn-sm">Invitar</button>
              </div>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>
                <span class="status-indicator bg-danger"></span>
                Mike Johnson
              </span>
              <div class="btn-group">
                <button class="btn btn-primary btn-sm">Mensaje</button>
                <button class="btn btn-danger btn-sm">Bloquear</button>
                <button class="btn btn-success btn-sm">Invitar</button>
              </div>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>
                <span class="status-indicator bg-danger"></span>
                Mike Johnson
              </span>
              <div class="btn-group">
                <button class="btn btn-primary btn-sm">Mensaje</button>
                <button class="btn btn-danger btn-sm">Bloquear</button>
                <button class="btn btn-success btn-sm">Invitar</button>
              </div>
            </li>
            <li class="list-group-item d-flex justify-content-between align-items-center">
              <span>
                <span class="status-indicator bg-danger"></span>
                Mike Johnson
              </span>
              <div class="btn-group">
                <button class="btn btn-primary btn-sm">Mensaje</button>
                <button class="btn btn-danger btn-sm">Bloquear</button>
                <button class="btn btn-success btn-sm">Invitar</button>
              </div>
            </li>
            
          </ul>
        </div>
      </div>
    </div>
    <div class="col-sm-6 mb-3">
      <div class="card h-100 card-scrollable">
        <div class="card-body card-body2">
          <h6 class="d-flex align-items-center mb-3">Friend Requests</h6>

          <!-- Contenido de solicitudes pendientes -->
          <div class="d-flex flex-column">
            <ul class="list-group">
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>
                  <span class="status-indicator bg-success"></span>
                  John Doe
                </span>
                <div class="btn-group">
                  <button class="btn btn-success btn-sm">Aceptar</button>
                  <button class="btn btn-danger btn-sm">Rechazar</button>
                </div>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                <span>
                  <span class="status-indicator bg-success"></span>
                  John Doe
                </span>
                <div class="btn-group">
                  <button class="btn btn-success btn-sm">Aceptar</button>
                  <button class="btn btn-danger btn-sm">Rechazar</button>
                </div>
              </li>
              
              <!-- Más solicitudes pendientes pueden añadirse aquí -->
            </ul>
          </div>

          <!-- Campo de búsqueda para enviar una solicitud de amistad -->
          <div class="search-friend mt-4">
            <input type="text" class="form-control" placeholder="Buscar usuario..." v-model="searchQuery">
            <button class="btn btn-primary mt-2 w-100" @click="sendFriendRequest">Enviar Solicitud</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import NavHome from './NavHome.vue'
</script>

<style scoped>
.friends-list {
  max-height: 200px; /* Limita la altura de la lista */
  overflow-y: auto;  /* Habilita la barra de desplazamiento vertical si el contenido es mayor */
}

.status-indicator {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 5px;
}

.bg-success {
  background-color: green;
}

.bg-danger {
  background-color: red;
}
.card-scrollable::-webkit-scrollbar {
  width: 8px;
}

.card-scrollable::-webkit-scrollbar-thumb {
  background-color: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}

.card-scrollable::-webkit-scrollbar-thumb:hover {
  background-color: rgba(0, 0, 0, 0.4);
}
.list-group-item {
  padding: 10px 20px; /* Aumenta el espacio interno */
  margin-bottom: 5px; /* Añade espacio entre los items */
}

.list-group-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
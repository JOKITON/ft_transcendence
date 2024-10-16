<template>
  <div class="chat-dropdown">
    <!-- Botón para mostrar/ocultar el dropdown -->
    <button
      @click="toggleDropdown"
      class="dropdown-toggle"
      :aria-expanded="isDropdownVisible.toString()"
    >
      Open Chats
    </button>

    <!-- Lista de chats desplegable -->
    <div v-if="isDropdownVisible" class="dropdown-list">
      <div class="scrollable-list">
        <ul v-if="friends.length">
          <li v-for="friend in friends" :key="friend.id">
            <button
              class="friend-button"
              @click="openChat(friend)"
              :disabled="friend.is_blocked_by_user || friend.is_blocked_by_friend"
            >
              {{ friend.username }}
              <!-- Indicador de estado -->
              <span
                :class="['status-indicator', friend.isOnline ? 'bg-success' : 'bg-danger']"
              ></span>
              <span v-if="friend.is_blocked_by_user" class="blocked-info"> (User blocked) </span>
              <span v-if="friend.is_blocked_by_friend" class="blocked-info">
                (You are blocked)
              </span>
            </button>

            <!-- Botones de bloqueo/desbloqueo -->
            <div class="btn-group">
              <button
                v-if="friend.is_blocked_by_user"
                class="btn btn-warning btn-sm"
                @click="unblockUser(friend.username)"
              >
                Unblock
              </button>
              <button
                v-else
                class="btn btn-danger btn-sm"
                @click="blockUser(friend.username)"
                :disabled="friend.is_blocked_by_friend"
              >
                Block
              </button>
            </div>
          </li>
        </ul>
        <p v-else>No friends available</p>
      </div>
    </div>

    <!-- Mostrar chats abiertos -->
    <div v-for="(chat, index) in activeChats" :key="chat.id" class="chat-container">
      <beautiful-chat
        :participants="[{ id: chat.friend.id, name: chat.friend.username }]"
        :messageList="chat.messages"
        :is-open="chat.isOpen"
        @open="handleChatOpen(index)"
        @close="handleChatClose(index)"
        @send-message="sendMessage(index, $event)"
        :placeholder="'Escribe un mensaje...'"
        :colors="colors"
        :alwaysScrollToBottom="true"
        :messageStyling="true"
        :open="() => openChat(lastOpenedChat.value)"
        :close="() => closeChat(index)"
        :onMessageWasSent="(message) => sendMessage(index, message)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject } from 'vue'
import Chat from 'vue3-beautiful-chat' // Importa el componente de chat
import Socket from '../../utils/socket/imp/socket'
import { WebsocketEvent } from 'websocket-ts'

interface Friend {
  id: number
  username: string
  isOnline: boolean
  is_blocked_by_user: boolean
  is_blocked_by_friend: boolean
}

interface Message {
  type: string
  author: string
  data: {
    text: string
  }
}

interface ChatInstance {
  id: number
  friend: Friend
  messages: Message[]
  isOpen: boolean
  newMessagesCount: number
}

const api = inject('$api') as any
const friends = ref<Friend[]>([])
const activeChats = ref<ChatInstance[]>([])
const isDropdownVisible = ref(false)
const lastOpenedChat = ref<Friend | null>(null)
const size = ref(1)
const socket = new Socket()
const user = ref('')
//const socket = inject('socket') as Socket | null

const colors = {
  header: {
    bg: '#584c66', // Mantener el color azul
    text: '#ffffff' // Texto blanco
  },
  launcher: {
    bg: '#223d5a' // Color de fondo del lanzador
  },
  messageList: {
    bg: '#f4f7f9' // Color de fondo de la lista de mensajes, más claro para contraste
  },
  sentMessage: {
    bg: '#6c7e90', // Color del mensaje enviado
    text: '#ffffff' // Texto blanco
  },
  receivedMessage: {
    bg: '#394c60', // Color del mensaje recibido
    text: '#ffffff' // Texto oscuro
  },
  userInput: {
    bg: '#223d5a', // Fondo del campo de entrada
    text: '#ffffff' // Texto en el campo de entrada
  }
}

const toggleDropdown = () => {
  isDropdownVisible.value = !isDropdownVisible.value
}

const openChat = (friend: Friend) => {
  console.log('Opening chat with:', friend)
  if (!friend) {
    friend = lastOpenedChat.value
  }
  // Cierra todos los chats abiertos
  activeChats.value.forEach((chat) => {
    chat.isOpen = false
  })

  // Verifica si ya existe un chat con ese amigo
  const existingChat = activeChats.value.find((chat) => chat.friend.id === friend.id)

  if (existingChat) {
    existingChat.isOpen = true
  } else {
    // Rellenar con mensajes de ejemplo
    // aqui se podrian cargar los mensajes del chat
    const messageList: Message[] = [
      //{ type: 'text', author: 'me', data: { text: 'Say yes!' } },
      //{ type: 'text', author: 'friend', data: { text: 'No.' } }
    ]

    activeChats.value.push({
      id: friend.id,
      friend,
      messages: messageList,
      isOpen: true,
      newMessagesCount: 0
    })
  }
  // Guarda el último amigo con el que se abrió el chat
  lastOpenedChat.value = friend
  console.log('Chat opened with:', lastOpenedChat.value)
}

// Función para cerrar el chat
const handleChatClose = (chatIndex: number) => {
  activeChats.value[chatIndex].isOpen = false
}

const closeChat = (chatIndex: number) => {
  activeChats.value[chatIndex].isOpen = false
}

// Función para abrir el chat
const handleChatOpen = (chatIndex: number) => {
  activeChats.value[chatIndex].isOpen = true
}

// Método para enviar mensajes
const sendMessage = (chatIndex: number, message: any) => {
  const chat = activeChats.value[chatIndex]
  const friend = chat.friend

  // Validar si tú o el amigo están bloqueados
  if (friend.is_blocked_by_user || friend.is_blocked_by_friend) {
    console.error('No puedes enviar mensajes. Tú o tu amigo están bloqueados.')
    return
  }

  if (message && message.data.text) {
    const text = message.data.text
    if (text.length > 0) {
      chat.newMessagesCount = chat.isOpen ? chat.newMessagesCount : chat.newMessagesCount + 1
      socket.send(user.value, text)
    }
  }
}

//const connectWebSocket = () => {}
// Función para agregar el mensaje a la lista de mensajes
const onMessageWasSent = (chatIndex: number, message: Message) => {
  const chat = activeChats.value[chatIndex]
  chat.messages = [...chat.messages, message]
  console.log('Message added: ', message)
}

// Carga la lista de amigos al montar el componente
onMounted(async () => {
  try {
    const response = await api.get<{ friends: Friend[] }>('friendship/friends')
    const Iam = await api.get('auth/iam')
    user.value = Iam.username
    console.log('User:', user.value)
    connectWebSocket()
    // Convertir isOnline a booleano
    friends.value = (response.friends || []).map((friend) => ({
      ...friend,
      isOnline: friend.isOnline === 'True' // Convertir a booleano
    }))

    console.log('Friends loaded:', friends.value)
  } catch (error) {
    console.error('Error fetching friends:', error)
  }
})

const echoOnMessage = (i: Websocket, ev: MessageEvent) => {
  const data = JSON.parse(ev.data)
  let username = data.username === user.value ? 'me' : 'friend'
  console.log('username', username)
  onMessageWasSent(0, {
    type: 'text',
    author: username,
    data: { text: data.message }
  })
}

const connectWebSocket = () => {
  socket.AddEventListener(WebsocketEvent.message, echoOnMessage)
}

// Función para bloquear un amigo
const blockUser = async (username: string) => {
  try {
    await api.post('friendship/blockFriend', { friend_username: username })
    console.log(`User ${username} blocked successfully`)
    friends.value = friends.value.map((friend) =>
      friend.username === username ? { ...friend, is_blocked_by_user: true } : friend
    )
  } catch (error) {
    console.error('Error blocking user', error)
  }
}

// Función para desbloquear un amigo
const unblockUser = async (username: string) => {
  try {
    await api.post('friendship/unblockFriend', { friend_username: username })
    console.log(`User ${username} unblocked successfully`)
    friends.value = friends.value.map((friend) =>
      friend.username === username ? { ...friend, is_blocked_by_user: false } : friend
    )
  } catch (error) {
    console.error('Error unblocking user', error)
  }
}
</script>

<style scoped>
.chat-dropdown {
  position: fixed;
  bottom: 0;
  width: 100%;
  padding: 10px;
  font-family: NunitoBlack, sans-serif;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.dropdown-toggle {
  background-color: #584c66;
  color: #ffffff;
  padding: 10px;
  border-radius: 5px;
  font-family: Titulo, sans-serif;
}

.dropdown-list {
  display: flex;
  justify-content: center;
  margin-top: 10px;
}

.dropdown-list ul {
  list-style: none;
  padding: 0;
  margin: 0;
  background-color: #aaa0a3;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 200px;
}

.dropdown-list li {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #ebd2ff;
  color: #fff;
  font-family: NunitoBlack, sans-serif;
  font-size: 14px;
}

.dropdown-list li:hover {
  background-color: hsl(221, 41%, 84%);
  cursor: pointer;
}

.dropdown-list li:last-child {
  border-bottom: none;
}
.friend-button {
  background: none;
  border: none;
  color: #6c7580;
  cursor: pointer;
  width: 100%;
  text-align: left;
  padding: 8px;
}
.status-indicator {
  width: 10px;
  height: 10px;
  display: inline-block;
  border-radius: 50%;
}

.bg-success {
  background-color: green;
}

.bg-danger {
  background-color: red;
}

.btn-group {
  display: flex;
  gap: 5px;
}

.blocked-info {
  font-size: 0.8em;
  color: red;
}
.scrollable-list {
  max-height: none;
  overflow-y: visible;
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>

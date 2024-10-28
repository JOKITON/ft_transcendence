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
        <p v-else class="no-friends-msg">No friends available</p>
      </div>
    </div>

    <!-- Mostrar chats abiertos -->

    <div v-for="chat in activeChats" :key="chat.id" class="chat-container">
      <beautiful-chat
        :participants="[{ id: chat.friend.id, name: chat.friend.username }]"
        :messageList="chat.messages"
        :is-open="chat.isOpen"
        @open="handleChatOpen(chat.id)"
        @close="handleChatClose(chat.id)"
        @send-message="sendMessage(chat.id, $event)"
        :placeholder="'Escribe un mensaje...'"
        :colors="colors"
        :alwaysScrollToBottom="true"
        :messageStyling="true"
        :open="() => openChat(lastOpenedChat)"
        :close="() => closeChat(chat.id)"
        :onMessageWasSent="(message) => sendMessage(chat.id, message)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, inject } from 'vue'
import Chat from 'vue3-beautiful-chat' // Importa el componente de chat
import Socket from '../../utils/socket/imp/socket'
import { WebsocketEvent } from 'websocket-ts'

import { eventBus } from './eventbus.js'

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
  socket?: Socket
}

const api = inject('$api') as any
const friends = ref<Friend[]>([])
const activeChats = ref<ChatInstance[]>([])
const isDropdownVisible = ref(false)
const lastOpenedChat = ref<Friend | null>(null)
const socket = new Socket()
const size = ref(1)
const user = ref('')
const room = ref('')
const room_id = ref('')
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

const openChat = async (friend: Friend) => {
  const whoami = await api.get('auth/whoami')
  console.log('Whoamiantes de room:', whoami)
  console.log('Friend antes de room:', friend)
  const response2 = await api.post('friendship/room', {
    friend_id: friend.id,
    user_id: whoami.id
  })
  console.log('response2:', response2)
  room.value = response2.room
  room_id.value = response2.room_id

  // Cierra todos los chats abiertos
  activeChats.value.forEach((chat) => {
    if (chat.socket) {
      chat.socket.close()
      chat.socket = null
    }
    chat.isOpen = false
    chat.messages = []
  })

  // Busca si ya existe un chat con este amigo
  const existingChat = activeChats.value.find((chat) => chat.id === room_id.value)

  if (existingChat) {
    existingChat.isOpen = true
    if (!existingChat.socket) {
      // Conecta solo si el socket no está abierto
      existingChat.socket = new Socket()
      existingChat.socket.open(room_id.value)
      connectWebSocket(existingChat.socket)
    }
    existingChat.messages = [];
  } else {
    const chat = {
      id: room_id.value,
      friend,
      messages: [],
      isOpen: true,
      newMessagesCount: 0,
      socket: new Socket()
    }
    chat.socket.open(room_id.value)
    connectWebSocket(chat.socket)
    activeChats.value.push(chat)
  }

  lastOpenedChat.value = friend
}


// Función para cerrar el chat
const handleChatClose = (chatId: number) => {
  const chat = activeChats.value.find((chat) => chat.id === chatId)
  chat.isOpen = false
  if (chat.socket) {
  chat.socket.close()
  chat.socket = null
  }
  chat.messages = []
  //activeChats.value[chatId].isOpen = false
}

const closeChat = (chatId: number) => {
  const chat = activeChats.value.find((chat) => chat.id === chatId)

  if (chat) {
    chat.isOpen = false
    if (chat.socket) {
      chat.socket.close()
      chat.socket = null
    }
    chat.messages = []
  }
}
// Función para abrir el chat
const handleChatOpen = (chatId: number) => {
  const chat = activeChats.value.find((chat) => chat.id === chatId)
  chat.isOpen = true
  //activeChats.value[chatIndex].isOpen = true
}
// Método para enviar mensajes
const sendMessage = (chatId: number, message: any) => {
  const chat = activeChats.value.find((chat) => chat.id === chatId)
  if (!chat || !chat.socket) {
    console.error('Socket no disponible para este chat.')
    return
  }
  console.log('message para guardaaaaar:', message)
  const text = message.data.text
  if (text.length > 0) {
    chat.newMessagesCount = chat.isOpen ? chat.newMessagesCount : chat.newMessagesCount + 1
    chat.socket.send(user.value, text, chatId) // Envía el mensaje a través del socket
  }
  console.log('user, text, chatId:', user.value, text, chatId)
}
// Función para agregar el mensaje a la lista de mensajes
/*const onMessageWasSent = (chatId: number, message: Message) => {
  console.log('entra en onMessageWasSent')
  console.log('ChatId:', chatId)
  console.log('Message:', message)
  const chat = activeChats.value.find((chat) => chat.id === chatId)
  //const chat = activeChats.value[chatId]
  chat.messages = [...chat.messages, message]
  console.log('Message added: ', message)
}
*/
const onMessageWasSent = (chatId: number, message: Message) => {
  const chat = activeChats.value.find((chat) => chat.id === chatId);
  
  if (!chat) return;

  const lastMessage = chat.messages[chat.messages.length - 1];

  // Verificar si el último mensaje es igual al nuevo
  const isDuplicate = lastMessage?.data.text === message.data.text && lastMessage?.author === message.author;

  if (!isDuplicate) {
    chat.messages = [...chat.messages, message];
  }
};


// Carga la lista de amigos al montar el componente
onMounted(async () => {
  try {
    const response = await api.get<{ friends: Friend[] }>('friendship/friends')
    activeChats.value.forEach((chat) => {
    if (chat.socket) {
      chat.socket.close();
      chat.socket = null;
    }
  });
    const Iam = await api.get('auth/iam')
    user.value = Iam.username
    console.log('User:', user.value)
    eventBus.on('messageSent', (data) => {
      console.log('Message sent:', data)
      openChat(data.friend)
    })
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
  const chatId = data.index
  const chat = activeChats.value.find((chat) => chat.id === chatId)
console.log('al entrar en echoOnMessage')
  if (chat) {
    onMessageWasSent(chatId, {
      type: 'text',
      author: data.username === user.value ? 'me' : 'friend',
      data: { text: data.message }
    })
  }
}

const connectWebSocket = (socketInstance: Socket) => {
  console.log('Connecting to websocket')
  socketInstance.AddEventListener(WebsocketEvent.message, echoOnMessage)
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
.chat-container {
  position: absolute;
  z-index: 1119; /* Valor por defecto para los chats */
}

.chat-container.active {
  position: absolute;
  z-index: 1111111; /* Valor más alto para el chat activo */
}

.no-friends-msg {
  background-color: #b8b5bd;
  color: #000000;
  padding: 10px;
  border-radius: 5px;
  text-align: center;
  font-family: NunitoBlack, sans-serif;
}
</style>

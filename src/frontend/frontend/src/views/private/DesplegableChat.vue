<template>
  <div class="chat-dropdown">
    <!-- Botón para mostrar/ocultar el dropdown -->
    <button @click="toggleDropdown" class="dropdown-toggle">
      Open Chats
    </button>

    <!-- Lista de chats desplegable -->
    <div v-if="isDropdownVisible" class="dropdown-list">
      <ul v-if="friends.length">
        <li v-for="friend in friends" :key="friend.id">
          <button 
            class="friend-button" 
            @click="openChat(friend)" 
            :disabled="friend.is_blocked_by_user || friend.is_blocked_by_friend"
          >
            {{ friend.username }} 
            <span v-if="friend.isOnline">(Online)</span>
            <span v-if="friend.is_blocked_by_user" class="blocked-info">
              (User blocked)
            </span>
            <span v-if="friend.is_blocked_by_friend" class="blocked-info">
              (You are blocked)
            </span>
          </button>
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
import { ref, onMounted, inject } from 'vue';
import Chat from 'vue3-beautiful-chat'; // Importa el componente de chat

interface Friend {
  id: number;
  username: string;
  isOnline?: boolean;
  is_blocked_by_user: boolean;
  is_blocked_by_friend: boolean;
}

interface Message {
  type: string;
  author: string;
  data: {
    text: string;
  };
}

interface ChatInstance {
  id: number;
  friend: Friend;
  messages: Message[];
  isOpen: boolean;
  newMessagesCount: number;
}

const api = inject('$api') as any;
const friends = ref<Friend[]>([]);
const activeChats = ref<ChatInstance[]>([]);
const isDropdownVisible = ref(false);
const lastOpenedChat = ref<Friend | null>(null);

const colors = {
  header: {
    bg: '#4e8cff',
    text: '#ffffff'
  },
  launcher: {
    bg: '#4e8cff'
  },
  messageList: {
    bg: '#ffffff'
  },
  sentMessage: {
    bg: '#4e8cff',
    text: '#ffffff'
  },
  receivedMessage: {
    bg: '#eaeaea',
    text: '#222222'
  },
  userInput: {
    bg: '#f4f7f9',
    text: '#565867'
  }
};

const toggleDropdown = () => {
  isDropdownVisible.value = !isDropdownVisible.value;
};

const openChat = (friend: Friend) => {
  console.log("Opening chat with:", friend);
  if (!friend) {
    friend = lastOpenedChat.value;
  }
  // Cierra todos los chats abiertos
  activeChats.value.forEach(chat => {
    chat.isOpen = false;
  });

  // Verifica si ya existe un chat con ese amigo
  const existingChat = activeChats.value.find(chat => chat.friend.id === friend.id);

  if (existingChat) {
    existingChat.isOpen = true;
  } else {
    // Rellenar con mensajes de ejemplo
    const messageList: Message[] = [
      { type: 'text', author: 'me', data: { text: 'Say yes!' } },
      { type: 'text', author: 'friend', data: { text: 'No.' } }
    ];
    
    activeChats.value.push({
      id: friend.id,
      friend,
      messages: messageList,
      isOpen: true,
      newMessagesCount: 0
    });
  }

  // Guarda el último amigo con el que se abrió el chat
  lastOpenedChat.value = friend;
  console.log("Chat opened with:", lastOpenedChat.value);
};

// Función para cerrar el chat
const handleChatClose = (chatIndex: number) => {
  activeChats.value[chatIndex].isOpen = false;
};

const closeChat = (chatIndex: number) => {
  activeChats.value[chatIndex].isOpen = false;
};

// Función para abrir el chat
const handleChatOpen = (chatIndex: number) => {
  activeChats.value[chatIndex].isOpen = true;
};

// Método para enviar mensajes
const sendMessage = (chatIndex: number, message: any) => {
  const chat = activeChats.value[chatIndex];
  const friend = chat.friend;

  // Validar si tú o el amigo están bloqueados
  if (friend.is_blocked_by_user || friend.is_blocked_by_friend) {
    console.error("No puedes enviar mensajes. Tú o tu amigo están bloqueados.");
    return;
  }

  if (message && message.data.text) {
    const text = message.data.text;
    if (text.length > 0) {
      chat.newMessagesCount = chat.isOpen ? chat.newMessagesCount : chat.newMessagesCount + 1;

      const newMessage: Message = {
        type: 'text',
        author: 'me', 
        data: { text }
      };

      // Agregar el mensaje a la lista de mensajes
      onMessageWasSent(chatIndex, newMessage);
    }
  } else {
    console.error("El mensaje no contiene texto válido.");
  }
};

// Función para agregar el mensaje a la lista de mensajes
const onMessageWasSent = (chatIndex: number, message: Message) => {
  const chat = activeChats.value[chatIndex];
  chat.messages = [...chat.messages, message];
  console.log("Message added: ", message);
};

// Carga la lista de amigos al montar el componente
onMounted(async () => {
  try {
    const response = await api.get<{ friends: Friend[] }>('friendship/friends');
    friends.value = response.friends || [];
  } catch (error) {
    console.error('Error fetching friends:', error);
  }
});

// Función para bloquear un amigo
const blockUser = async (username: string) => {
  try {
    await api.post('friendship/blockFriend', { friend_username: username });
    console.log(`User ${username} blocked successfully`);
    friends.value = friends.value.map(friend =>
      friend.username === username ? { ...friend, is_blocked_by_user: true } : friend
    );
  } catch (error) {
    console.error('Error blocking user', error);
  }
};

// Función para desbloquear un amigo
const unblockUser = async (username: string) => {
  try {
    await api.post('friendship/unblockFriend', { friend_username: username });
    console.log(`User ${username} unblocked successfully`);
    friends.value = friends.value.map(friend =>
      friend.username === username ? { ...friend, is_blocked_by_user: false } : friend
    );
  } catch (error) {
    console.error('Error unblocking user', error);
  }
};
</script>

<style scoped>
.chat-dropdown {
  position: fixed;
  bottom: 0;
  width: 100%;
  padding: 10px;
  text-align: center;
}

.dropdown-toggle {
  background-color: #007bff;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
}

.dropdown-list {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  background-color: white;
  border: 1px solid #ddd;
  max-height: 200px;
  overflow-y: auto;
  width: 20%;
  margin-top: 10px;
  z-index: 1000;
}

.dropdown-list ul {
  list-style: none;
  padding: 0;
}

.dropdown-list li {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.dropdown-list li:last-child {
  border-bottom: none;
}

.friend-button {
  width: 100%;
  padding: 10px 15px;
  background-color: #f4f4f4;
  border: none;
  text-align: left;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
}

.friend-button:hover {
  background-color: #eaeaea;
}

.blocked-info {
  color: red;
  font-weight: bold;
}

.btn-group {
  display: flex;
  gap: 5px;
}
</style>

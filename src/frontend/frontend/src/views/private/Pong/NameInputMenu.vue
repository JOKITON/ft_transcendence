<template>
    <div class="form-container">
        <div class="form-content">
            <form @submit.prevent="startGame" class="game-form">
                <div class="d-flex justify-content-center mt-4">
                    <!-- Toggle buttons for Online/Offline mode -->
                    <button type="button" class="btn btn-lg mx-2"
                        :class="{ 'btn-primary': isOnline === 'Online', 'btn-outline-primary': isOnline !== 'Online' }"
                        @click="setGameMode('Online')">
                        Online
                    </button>
                    <button type="button" class="btn btn-lg mx-2"
                        :class="{ 'btn-secondary': isOnline === 'Offline', 'btn-outline-secondary': isOnline !== 'Offline' }"
                        @click="setGameMode('Offline')">
                        Offline
                    </button>
                </div>

                <div v-if="isOnline" class="player-inputs">
                    <h3 class="mb-3">Choose Game Mode:</h3>
                    <div class="game-mode-options">
                        <label v-if="isOnline === 'Offline'" class="game-mode-label">
                            <input v-model="gameMode" type="radio" value="onePlayer" required />
                            One Player (vs AI)
                        </label>
                        <label class="game-mode-label">
                            <input v-model="gameMode" type="radio" value="twoPlayer" required />
                            Two Player
                        </label>
                        <label class="game-mode-label">
                            <input v-model="gameMode" type="radio" value="eightPlayer" required />
                            Tournament (4|8 Player)
                        </label>
                    </div>
                </div>

                <!-- Player Input Fields -->
                <div v-if="gameMode" class="player-inputs">
                    <span v-if="gameMode === 'onePlayer'" class="vs-text">{{ userOne.nickname }} VS AI</span>

                    <div v-if="gameMode !== 'onePlayer'" class="player-group">
                        <span class="player-nickname">{{ userOne.nickname }}</span>
						<span class="vs-text">VS</span>
                        <div class="player-group">
                            <!-- Inside your player group for two-player mode -->
                            <div v-if="gameMode === 'twoPlayer'" class="player-group">
                                <select v-model="selectedOpponent" class="form-select" required>
                                    <option value="" disabled>Select Opponent</option>
                                    <option v-for="user in orUsers" :key="user.nickname" :value="user.nickname">
                                        {{ user.nickname }}
                                    </option>
                                </select>
                            </div>

                            <!-- Inside your player group for eight-player mode -->
                            <div v-if="gameMode === 'eightPlayer' && (users.length == 4 || users.length == 8)">
                                <div v-for="(user, index) in users" :key="index" class="player-group">
                                    <select v-model="user.nickname" class="form-select" required>
                                        <option value="" disabled>Select Opponent</option>
                                        <option v-for="filteredUser in filteredUsers(index)" :key="filteredUser.nickname" :value="filteredUser.nickname">
                                            {{ filteredUser.nickname }}
                                        </option>
                                    </select>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- AI Difficulty Selection for One Player Mode -->
                    <div v-if="gameMode === 'onePlayer'" class="ai-difficulty">
                        <select v-model="aiDifficulty" class="form-select" required>
                            <option value="">Choose difficulty...</option>
                            <option value="0.3">Easy</option>
                            <option value="0.5">Normal</option>
                            <option value="1">Hard</option>
                            <option value="1.5">Impossible</option>
                        </select>
                    </div>
                </div>

                <button
                    v-if="gameMode && (gameMode === 'onePlayer' || (gameMode === 'twoPlayer' && users.length >= 2) || (gameMode === 'eightPlayer' && (users.length == 4 || users.length == 8)))"
                    type="submit" class="btn btn-primary mt-4">Start Game</button>
            </form>

            <!-- Leaderboard Section -->
            <div class="leaderboard mt-10000">
                <h6 class="d-flex align-items-center mb-3">Leaderboard</h6>
                <ul class="list-group">
                    <li v-for="user in leaderboard" :key="user.id"
                        class="list-group-item d-flex justify-content-between align-items-center">
                        <span>
                            <span :class="['status-indicator', user.status]"></span>
                            {{ user.name }}
                        </span>
                        <span class="badge bg-primary rounded-pill">{{ user.score }}</span>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed, inject } from 'vue';
import type Api from '@/utils/Api/Api'
import auth from '../../../services/user/services/auth/auth.ts'

const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)

const isOnline = ref(''); // Keep track of whether Online or Offline is selected
const gameMode = ref('');
const aiDifficulty = ref(1);
const selectedOpponent = ref('');

// Sample leaderboard data
const leaderboard = ref([
    { id: 1, name: 'Jane Smith', score: 1500, status: 'bg-success' },
    { id: 2, name: 'Mike Johnson', score: 1200, status: 'bg-danger' },
    { id: 3, name: 'Emily Davis', score: 1000, status: 'bg-success' },
    { id: 4, name: 'Chris Brown', score: 800, status: 'bg-danger' },
]);

onMounted(async () => {
    await fetchNickname()
    await fetchUserList()
})

interface User {
    id: number;
    username: string;
    nickname: string;
    status: string;
}

const users = ref<User[]>([]);
const orUsers = ref<User[]>([]);
const userOne = ref<User>(); // Assuming you want to store the fetched user

const fetchUserList = async () => {
    try {
        const response = await api.get<User[]>('friendship/users');
        users.value = response.data || [];

		orUsers.value = [...users.value];

        // Add the user from fetchNickname() at the first position
        if (userOne.value) {
            users.value.unshift(userOne.value); // Add the user to the start of the array
        }

        /* users.value.forEach(user => {
            console.log(user.username);
        }); */
    } catch (error) {
        console.error('Error fetching users:', error.response ? error.response.data : error.message);
    }
}

async function fetchNickname() {
    try {
        const response = await Auth.whoami();
        userOne.value = {
            id: response.id,
            username: response.username,
            nickname: response.nickname,
            status: 'Online',
        };
    } catch (error: any) {
        console.error('Error fetching user data:', error.message);
    }
}

const emit = defineEmits(['startGame']);

// Function to set the game mode (Online/Offline)
const setGameMode = (mode) => {
    isOnline.value = mode;
    gameMode.value = ''; // Reset game mode when switching between Online/Offline
};

const filteredUsers = (currentIndex) => {
    return users.value.filter(user =>
        !users.value.some((selectedUser, index) => index !== currentIndex && selectedUser.nickname === user.nickname && selectedUser.nickname !== userOne.nickname)
    );
};

const startGame = () => {
    const data = {
        gameMode: gameMode.value,
        players: users.value.map(user => ({
            player: user.nickname,
            id: user.id,
        })),
    };

    if (gameMode.value === 'onePlayer') {
        data.aiDifficulty = aiDifficulty.value;
    }

    emit('startGame', data);
};
</script>

<style scoped>
.form-container {
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 2rem;
	padding-top: 100px;
}

.form-content {
	background-color: white;
	padding: 20px;
	border-radius: 8px;
	box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h3 {
	font-family: 'Roboto', sans-serif;
	font-weight: 500;
	color: #333;
}

.game-mode-options {
	display: flex;
	justify-content: space-between;
	gap: 10px;
}

.game-mode-label {
	font-family: 'Roboto', sans-serif;
	font-size: 1rem;
	cursor: pointer;
	color: #495057;
	transition: color 0.2s ease;
}

.game-mode-label:hover {
	color: #007bff;
}

.player-inputs {
	margin-top: 1rem;
}

.player-group {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 1rem;
}

.form-control {
	flex: 1;
	padding: 0.5rem;
	border: 1px solid #ced4da;
	border-radius: 8px;
	font-size: 1rem;
	transition: border-color 0.2s ease;
}

.form-control:focus {
	border-color: #007bff;
	box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
	outline: none;
}

.vs-text {
	font-weight: bold;
	color: #6c757d;
	margin: 0 10px;
}

.btn {
	width: 100%;
	border-radius: 8px;
	padding: 0.75rem;
	font-size: 1.25rem;
	font-weight: 500;
	transition: background-color 0.2s ease;
}

.btn-primary {
	background-color: #007bff;
	border: none;
}

.btn-primary:hover {
	background-color: #0056b3;
}

.leaderboard {
	margin-top: 2rem;
}

.list-group-item {
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.status-indicator {
	display: inline-block;
	width: 10px;
	height: 10px;
	border-radius: 50%;
	margin-right: 10px;
}

.bg-success {
	background-color: #28a745;
}

.bg-danger {
	background-color: #dc3545;
}
</style>
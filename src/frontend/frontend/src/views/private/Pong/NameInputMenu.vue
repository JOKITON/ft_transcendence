<template>
    <div class="form-container">
        <div class="form-content">
            <h2 class="title">Play Menu</h2>
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
                            <input v-model="gameMode" type="radio" value="AI" required />
                            One Player (vs AI)
                        </label>
                        <label class="game-mode-label">
                            <input v-model="gameMode" type="radio" value="2P" required />
                            Two Player
                        </label>
                        <label class="game-mode-label">
                            <input v-model="gameMode" type="radio" value="4P" required />
                            Tournament (4|8 Player)
                        </label>
                    </div>
                </div>

                <!-- Player Input Fields -->
                <div v-if="gameMode" class="player-inputs">
                    <span v-if="gameMode === 'AI'" class="vs-text">
                        {{ userOne.nickname }} VS AI
                        <div class="form-check form-switch" style="margin-left: 10px;">
                            <input class="form-check-input" type="checkbox" v-model="isAudioEnabled" id="audioSwitch">
                            <label class="form-check-label" for="audioSwitch">Enable Audio</label>
                        </div>
                    </span>
                
                    <div v-if="gameMode !== 'AI'" class="player-group">
                        <div class="player-group">
                            <!-- Inside your player group for two-player mode -->
                            <div v-if="gameMode === '2P'" class="player-group">
                                <span class="player-nickname">{{ userOne.nickname }}</span>
                                <span class="vs-text">VS</span>
                                <select class="form-select" required>
                                    <option value="" disabled>Select Opponent</option>
                                    <option v-for="user in orUsers" :key="user.nickname" :value="user.nickname">
                                        {{ user.nickname }}
                                    </option>
                                </select>
                            </div>
                
                            <!-- Inside your player group for eight-player mode -->
                            <div v-if="gameMode === '4P' && (users.length == 4 || users.length == 8)">
                                <div v-for="(user, index) in users" :key="index" class="player-group">
                                    <!-- The player that should be in the left side of the column for the Tournament -->
                                    <div v-if="index % 2 == 0" class="player-select-wrapper" style="display: flex; align-items: center;">
                                        <select class="form-select" required>
                                            <option value="" disabled>Select Opponent</option>
                                            <option v-for="filteredUser in filteredUsers(index)" :key="filteredUser.nickname" :value="filteredUser.nickname">
                                                {{ filteredUser.nickname }}
                                            </option>
                                        </select>
                                        <span class="vs-text" style="margin-left: 10px;">VS</span>
                                        <select class="form-select" required>
                                            <option value="" disabled>Select Opponent</option>
                                            <option v-for="filteredUser in filteredUsers(index + 1)" :key="filteredUser.nickname" :value="filteredUser.nickname">
                                                {{ filteredUser.nickname }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- AI Difficulty Selection for One Player Mode -->
                    <div v-if="gameMode === 'AI'" class="ai-difficulty">
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
                    v-if="gameMode && (gameMode === 'AI' || (gameMode === '2P' && users.length >= 2) || (gameMode === '4P' && (users.length == 4 || users.length == 8)))"
                    type="submit" class="btn btn-primary mt-4">Start Game</button>
            </form>
             </div>
            <div class="trophy-container">
		        <img :src="img1" alt="Trophy" class="trophy-image" />
	        </div>
            <!-- Leaderboard Section -->
            <div class="leaderboard-container">
            <div v-if="gameMode == false" class="leaderboard">
                <h6 class="leaderboard-title">Leaderboard</h6>
                <ul class="list-group">
                    <li v-for="(user, index) in leaderboard" :key="user.id"
                        class="list-group-item d-flex justify-content-between align-items-center">
                        <span class="badge text-dark" >
                            <span v-if="user.status == 'True'" :class="['status-indicator', 'bg-success']"></span>
                            <span v-else-if="user.status == 'Offline'" :class="['status-indicator', 'bg-danger']"></span>
                            <span v-else :class="['status-indicator', 'bg-warning']"></span>
                            {{ user.name }}
                        </span>
                        <span class="badge bg-primary rounded-pill">{{ user.wins }}</span>
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
import img1 from '../../../assets/avatars/trofeo.png';

const api: Api = inject('$api') as Api
const Auth: auth = new auth(api)

const isOnline = ref(''); // Keep track of whether Online or Offline is selected
const gameMode = ref('');
const isAudioEnabled : boolean = ref(false);
const aiDifficulty = ref(1);
const selectedOpponent = ref('');

// Sample leaderboard data
const leaderboard = ref<LeaderboardEntry[]>([]); // Initialize the leaderboard as a single array of LeaderboardEntry objects

// Function to print the length of the leaderboard array
function printLeaderboardLength() {
  console.log(leaderboard.value.length);
}

onMounted(async () => {
    await fetchNickname()
    await fetchUserList()
    await fetchLeaderboard()
})

interface LeaderboardEntry {
    id: number;
    name: string;
    wins: number;
    status: string;
}

interface User {
    id: number;
    username: string;
    nickname: string;
    status: string;
}

const users = ref<User[]>([]);
const orUsers = ref<User[]>([]);
const userOne = ref<User>(); // Assuming you want to store the fetched user

// Set the default leaderboard data
const setDefaultLeaderboard = async () => {
    leaderboard.value = [{ id: 0, name: 'No data found', wins: 0, status: 'Offline' }];
}

const fetchLeaderboard = async () => {
    try {
        const response = await api.get('pong/leaderboard');
        if (response.data.length == 0) {
            console.log('No data found');
            setDefaultLeaderboard();
        }
        else {
            leaderboard.value = response.data as LeaderboardEntry[] || []; // Ensure you access the data property

            for (let i = 0; i < users.value.length; i++) {
                for (let j = 0; j < users.value.length; j++) {
                    if (leaderboard.value[i].name === users.value[j].nickname) {
                        leaderboard.value[i].status = users.value[j].status;
                    }
                }
            }
        }
    } catch (error) {
        console.error('Error fetching leaderboard:', error.response ? error.response.data : error.message);
    }
}

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
            status: 'True',
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
        !users.value.some((selectedUser, index) => index !== currentIndex && selectedUser.nickname === user.nickname)
    );
};

const startGame = () => {
    const data = {
        gameMode: gameMode.value,
        players: [],
        isAudioEnabled: isAudioEnabled.value,
    };

    if (gameMode.value === 'AI') {
        data.players.push({
            player: userOne.value.nickname,
            id: userOne.value.id,
        });
        data.aiDifficulty = aiDifficulty.value;
    } else if (gameMode.value === '2P') {
        const selectedOpponent = document.querySelector('.player-group select').value;
        const opponent = users.value.find(user => user.nickname === selectedOpponent);
        if (opponent) {
            data.players.push({
                player: userOne.value.nickname,
                id: userOne.value.id,
            });
            data.players.push({
                player: opponent.nickname,
                id: opponent.id,
            });
        }
    } else if (gameMode.value === '4P') {
        const selects = document.querySelectorAll('.player-select-wrapper select');
        selects.forEach(select => {
            const selectedNickname = select.value;
            const selectedUser = users.value.find(user => user.nickname === selectedNickname);
            if (selectedUser) {
                data.players.push({
                    player: selectedUser.nickname,
                    id: selectedUser.id,
                });
            }
        });
    }

    console.log('Data :', data);
    emit('startGame', data);
};
</script>

<style scoped>
.form-container {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: space-between;
	padding: 2rem;
	padding-top: 100px;
}

.form-content {
	background-color: #f9f9f9;
	padding: 30px;
	border-radius: 16px;
	box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
	width: 100%;
	max-width: 500px;
	font-family: Titulo, sans-serif;
}

.title {
	font-family: Titulo, sans-serif;
	font-size: 2rem;
	color: #007bff;
	margin-bottom: 1.5rem;
	text-align: center;
}

.game-form {
	width: 100%;
}
.toggle-btn {
	font-size: 1.2rem;
	font-weight: bold;
	padding: 0.75rem 1.5rem;
	border-radius: 12px;
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
	font-size: 1.2rem;
	color: #495057;
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
	background-color: #2c3e50;
	padding: 1.5rem;
	border-radius: 20px;
	box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
	width: 100%;
	max-width: 500px;
}
.list-group-item {
	background-color: #34495e;
	border-radius: 12px;
	color: #ecf0f1;
	border: none;
	margin-bottom: 0.5rem;
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
.trophy-image {
	width: 150px;
	height: auto;
    justify-content: center;
}
.trophy-container {
	margin-top: 2rem;
    justify-content: center;
}
.leaderboard-container {
	margin-top: 2rem;
	display: flex;
	justify-content: center;
	align-items: center;
}
.leaderboard-title {
	font-family: Titulo, sans-serif;
	font-size: 1.5rem;
	color: #ecf0f1;
	text-align: center;
	margin-bottom: 1rem;
}


</style>

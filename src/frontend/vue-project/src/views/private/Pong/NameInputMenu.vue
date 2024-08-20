<template>
	<div class="form-container">
		<form @submit.prevent="startGame" class="form-content">
			<h3 class="mb-3">Choose Game Mode:</h3>
			<div class="game-mode-options">
				<label class="game-mode-label">
					<input v-model="gameMode" type="radio" value="onePlayer" required />
					One Player (vs AI)
				</label>
				<label class="game-mode-label">
					<input v-model="gameMode" type="radio" value="twoPlayer" required />
					Two Player
				</label>
				<label class="game-mode-label">
					<input v-model="gameMode" type="radio" value="eightPlayer" required />
					Tournament (8 Player)
				</label>
			</div>

			<!-- Player Input Fields -->
			<div v-if="gameMode" class="player-inputs">
				<div v-for="(player, index) in filteredPlayers" :key="index" class="player-group">
					<input v-model="players[index].name1" :placeholder="'Enter Player ' + (index * 2 + 1) + ' Name'"
						class="form-control" required />
					<span v-if="gameMode !== 'onePlayer'" class="vs-text">VS</span>
					<input v-if="gameMode !== 'onePlayer'" v-model="players[index].name2"
						:placeholder="'Enter Player ' + (index * 2 + 2) + ' Name'" class="form-control" required />
				</div>

				<!-- AI Difficulty Selection for One Player Mode -->
				<div v-if="gameMode === 'onePlayer'" class="ai-difficulty">
					<select v-model="aiDifficulty" class="form-select" required>
						<option value="">Choose difficulty...</option>
						<option value="1">Easy</option>
						<option value="2">Normal</option>
						<option value="4">Hard</option>
						<option value="15">Impossible</option>
					</select>
				</div>
			</div>

			<button v-if="gameMode" type="submit" class="btn btn-primary mt-4">Start Game</button>
		</form>
	</div>
</template>

<script setup>
import { ref, computed } from 'vue';

const gameMode = ref('');
const aiDifficulty = ref(1);
const players = ref([
	{ name1: '', name2: '' },
	{ name1: '', name2: '' },
	{ name1: '', name2: '' },
	{ name1: '', name2: '' }
]);

// Compute the number of player pairs needed based on the game mode
const filteredPlayers = computed(() => {
	if (gameMode.value === 'onePlayer' || gameMode.value === 'twoPlayer') {
		return players.value.slice(0, 1);
	} else if (gameMode.value === 'eightPlayer') {
		return players.value;
	}
	return [];
});

const emit = defineEmits(['startGame']);

const startGame = () => {
	const data = {
		gameMode: gameMode.value,
		players: players.value.map(player => ({
			player1Name: player.name1,
			player2Name: player.name2
		}))
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

.form-control {
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

.btn-primary {
	background-color: #0056b3;
}
</style>
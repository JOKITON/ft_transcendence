<template>
	<div class="form-container d-flex align-items-center justify-content-center py-4">
		<div class="menu form-content">
			<form @submit.prevent="startGame">
				<div class="form-group mb-4">
					<h3 class="mb-3">Choose Game Mode:</h3>
					<div class="game-mode-options d-flex justify-content-between">
						<label class="game-mode-label">
							<input v-model="gameMode" type="radio" value="onePlayer" required /> One Player (vs AI)
						</label>
						<label class="game-mode-label">
							<input v-model="gameMode" type="radio" value="twoPlayer" required /> Two Player
						</label>
						<label class="game-mode-label">
							<input v-model="gameMode" type="radio" value="eightPlayer" required /> Tournament (8 Player)
						</label>
					</div>
				</div>

				<div v-if="gameMode === 'onePlayer'" class="form-group mb-3">
					<label class="form-label" for="player1">Player 1:</label>
					<input v-model="player1Name" id="player1" type="text" class="form-control" required placeholder="Enter Player 1 Name" />
				</div>

				<div v-if="gameMode === 'twoPlayer'" class="form-group mb-3">
					<label class="form-label" for="player1">Player 1:</label>
					<input v-model="player1Name" id="player1" type="text" class="form-control" required placeholder="Enter Player 1 Name" />
					<label class="form-label" for="player2">Player 2:</label>
					<input v-model="player2Name" id="player2" type="text" class="form-control" required placeholder="Enter Player 2 Name" />
				</div>

				<div v-if="gameMode === 'eightPlayer'" class="form-group mb-3 players-tournament">
					<label class="form-label" for="player1">Player 1:</label>
					<input v-model="player1Name" id="player1" type="text" class="form-control" required placeholder="Enter Player 1 Name" />
					<label class="form-label" for="player2">Player 2:</label>
					<input v-model="player2Name" id="player2" type="text" class="form-control" required placeholder="Enter Player 2 Name" />
					<label class="form-label" for="player3">Player 3:</label>
					<input v-model="player3Name" id="player3" type="text" class="form-control" required placeholder="Enter Player 3 Name" />
					<label class="form-label" for="player4">Player 4:</label>
					<input v-model="player4Name" id="player4" type="text" class="form-control" required placeholder="Enter Player 4 Name" />
					<label class="form-label" for="player5">Player 5:</label>
					<input v-model="player5Name" id="player5" type="text" class="form-control" required placeholder="Enter Player 5 Name" />
					<label class="form-label" for="player6">Player 6:</label>
					<input v-model="player6Name" id="player6" type="text" class="form-control" required placeholder="Enter Player 6 Name" />
					<label class="form-label" for="player7">Player 7:</label>
					<input v-model="player7Name" id="player7" type="text" class="form-control" required placeholder="Enter Player 7 Name" />
					<label class="form-label" for="player8">Player 8:</label>
					<input v-model="player8Name" id="player8" type="text" class="form-control" required placeholder="Enter Player 8 Name" />
				</div>

				<button type="submit" class="btn btn-primary btn-block mt-4">Start Game</button>
			</form>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';

const player1Name = ref('');
const player2Name = ref('');
const gameMode = ref('');

const emit = defineEmits(['startGame']);

const startGame = () => {
	emit('startGame', {
		gameMode: gameMode.value,
		player1Name: player1Name.value,
		player2Name: player2Name.value,
	});
};
</script>

<style scoped>
/* Centering the content */
.form-container {
	min-height: 100vh;
}

.form-content {
	background-color: white;
	padding: 20px;
	border-radius: 10px;
	box-shadow: 0px 8px 16px rgba(198, 35, 35, 0.1);
	max-width: 500px;
	width: 100%;
}

/* Headings */
h3 {
	font-family: 'Roboto', sans-serif;
	font-weight: 500;
	color: #333;
	margin-bottom: 1rem;
}

/* Game mode options styling */
.game-mode-options {
	display: flex;
	flex-wrap: wrap;
	justify-content: space-between;
	gap: 10px;
}

.game-mode-label {
	display: flex;
	align-items: center;
	font-family: 'Roboto', sans-serif;
	font-size: 1rem;
	cursor: pointer;
	color: #495057;
	transition: color 0.2s ease;
}

.game-mode-label input {
	margin-right: 8px;
}

/* Hover and active state */
.game-mode-label:hover {
	color: #007bff;
}

input:checked + .game-mode-label {
	color: #007bff;
}

/* Inputs */
.form-control {
	height: calc(1.5em + 0.75rem + 2px);
	border-radius: 8px;
	padding: 0.5rem;
	border: 1px solid #ced4da;
	font-size: 1rem;
	transition: border-color 0.2s ease;
}

.form-control:focus {
	border-color: #007bff;
	box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
	outline: none;
}

/* Button */
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

.players-tournament {
	display: grid;
	grid-template-columns: 1fr 1fr;
	gap: 15px;
}

@media (max-width: 576px) {
	.players-tournament {
		grid-template-columns: 1fr;
	}
}
</style>

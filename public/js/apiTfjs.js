const NUMBER_OF_MCTS_SIMULATIONS = 100
//public

function setupApi() {
	console.log("Importing dependencies ...")
	return importFromUrl("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@0.13.0")
	.then(() => {return importFromUrl("js/tfjs/utils.js")})
	.then(() => {return importFromUrl("js/tfjs/MCTS.js")})
	.then(() => {return importFromUrl("js/tfjs/tk/keras/NNet.js")})
	.then(() => {return importFromUrl("js/tfjs/TKLogick.js")})
	.then(() => {return importFromUrl("js/tfjs/TKGame.js")})
	.then(() => {
		console.log("Dependencies imported")
		return new NNet().load()
	})
	// .then(() => {return importFromUrl("/js/tfjs/tk/test/testTKLogick.js")}) // uncomment for tests
	// .then(() => {launchTests(); return Promise.resolve()}) // uncomment for tests
	.then(() => {console.log("Ready to play"); return Promise.resolve()})
}


function predictAction(data){
	return new Promise((resolve,reject) => {
		const
		player = data.player
		let
		state = data.board_state
		state = state.concat(data.players_scores)
		state = state.concat(data.players_tuz)
		const
		encoded_state = generate_encoded_state(state),

		game = new TKGame(),
		nnet = new NNet(),
		args = {
			numMCTSSims:NUMBER_OF_MCTS_SIMULATIONS,
			cpuct:1
		},
		mcts = new MCTS(game, nnet, args),

		canonical_form = game.getCanonicalForm(encoded_state, player)
		let
		action = argmax(mcts.getActionProb(canonical_form, temp=0))
		resolve({action:action})
	})
}

function getNextState(data){
	let
	player = data.player,
	action = data.action,
	prev_state = data.board_state
	prev_state = prev_state.concat(data.players_scores)
	prev_state = prev_state.concat(data.players_tuz)

	let
	prev_encoded_state = generate_encoded_state(prev_state),
	board = new Board()

	board.set_encoded_state(prev_encoded_state)
	board.execute_move(action, player)

	let
	next_player = -player,
	next_player_legal_moves = board.get_legal_moves(next_player),
	
	state = board.get_pieces(),
	players_scores = board.get_players_scores(),
	players_tuz = board.get_players_tuz()

	winner = null
	if (board.is_win(1,player))
		winner = 1
	else if (board.is_win(-1,player))
		winner = -1


	return Promise.resolve({
		next_player					: next_player,
		next_player_legal_moves		: next_player_legal_moves,
		state						: state,
		players_scores				: [players_scores[1],players_scores[-1]],
		players_tuz					: [players_tuz[1],players_tuz[-1]],
		winner						: winner
	})
}



// utils
function importFromUrl(url){
	return new Promise((resolve, reject) => {
		let script = document.createElement('script')
		script.onload = resolve
		script.src = url
		document.body.appendChild(script);
	})
}

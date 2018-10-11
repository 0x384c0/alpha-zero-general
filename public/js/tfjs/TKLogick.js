const
// WIDTH = 9, //already defined in game.js
// HEIGHT = 2, //already defined in game.js

INIT_BALLS_COUNT_IN_PIT = 9,

MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE = 1,
// BOARD_SIZE =  WIDTH * HEIGHT,  //already defined in game.js
WIN_SCORE = (BOARD_SIZE * WIDTH)/HEIGHT,

PIT_STATE_ENCODER = array_to_array_without_none, // data_array_to_one_hot_with_shape
PIT_STATE_DECODER = array_without_none_to_array, // one_hot_batch_to_array

SCORE_ENCODER = number_to_number_without_none,
SCORE_DECODER = number_without_none_to_number,

TUZ_ENCODER = number_to_number_without_none, // number_to_onehot
TUZ_DECODER = number_without_none_to_number // onehot_to_number

class Board{


	constructor(){

		const __additional_components_count = 4
		this.shape = [BOARD_SIZE + __additional_components_count, MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE]
		this.action_size = BOARD_SIZE


		this.__size = WIDTH * HEIGHT
		this.__init_state = new Array(BOARD_SIZE).fill(INIT_BALLS_COUNT_IN_PIT)

		this.__pieces = this.__init_state
		this.__players_scores = {
			"1"		:	0,	// player 1
			"-1"	:	0	// player -1
		}
		this.__players_tuz = {
			"1"		:	null,	// player 1
			"-1"	:	null	// player -1
		}
		this.__canonical_player = 1
	}

	get_encoded_state(){
		let pieces = this.__pieces
		let mid = int(pieces.length / 2)
		let half_shape = [int(this.shape[0]/2), this.shape[1]]

		// print(pieces)
		// print(mid)
		// print(pieces.slice(0,mid))
		// print(PIT_STATE_ENCODER(pieces.slice(0,mid),half_shape))

		let firstHalf = PIT_STATE_ENCODER(pieces.slice(0,mid),half_shape)
		firstHalf[WIDTH - 1 + 1] = SCORE_ENCODER(this.__players_scores[1 * this.__canonical_player],			MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
		firstHalf[WIDTH - 1 + 2] = TUZ_ENCODER(this.__players_tuz[1 * this.__canonical_player],					MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)

		let secondHalf = PIT_STATE_ENCODER(pieces.slice(-mid),half_shape)
		secondHalf[WIDTH - 1 + 1] = SCORE_ENCODER(this.__players_scores[-1 * this.__canonical_player],			MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
		secondHalf[WIDTH - 1 + 2] = TUZ_ENCODER(this.__players_tuz[-1 * this.__canonical_player],				MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
		
		if (this.__canonical_player == 1)
			secondHalf = operationWith2DArray(secondHalf, -1, "*")
		else
			firstHalf = operationWith2DArray(firstHalf, -1, "*")

		let result = concatenate(firstHalf, secondHalf)

		return result
	}
	set_encoded_state(i_state){
		let state = copy(i_state) // clone
		
		let mid = int(state.length / 2)
		let firstHalf = state.slice(0,mid)
		let secondHalf = state.slice(-mid)
		let firstSum = 0
		let secondSum = 0

		for (let onehot of firstHalf){
			firstSum += sum(onehot)
		}

		for (let onehot of secondHalf){
			secondSum += sum(onehot)
		}

		if (firstSum > 0 || secondSum < 0) {//  playe 1 in firstHalf
			this.__canonical_player = 1
			secondHalf = operationWith2DArray(secondHalf, -1, "*")
		} else {// player -1 in firstHalf
			this.__canonical_player = -1
			firstHalf = operationWith2DArray(firstHalf, -1, "*")
		}

		const HALF_BOARD_SIZE = int(BOARD_SIZE/2)

		// first half of board
		this.__pieces 				= PIT_STATE_DECODER(firstHalf.slice(0,HALF_BOARD_SIZE)) //  pit states
		this.__players_scores[1 * this.__canonical_player]	= SCORE_DECODER(firstHalf[HALF_BOARD_SIZE]) //  score
		this.__players_tuz[1 * this.__canonical_player]		= TUZ_DECODER(firstHalf[HALF_BOARD_SIZE + 1]) //  tuz position
		// second half of board
		this.__pieces = this.__pieces.concat(PIT_STATE_DECODER(secondHalf.slice(0,HALF_BOARD_SIZE))) //  pit states 
		this.__players_scores[-1 * this.__canonical_player]	= SCORE_DECODER(secondHalf[HALF_BOARD_SIZE]) //  score
		this.__players_tuz[-1 * this.__canonical_player]		= TUZ_DECODER(secondHalf[HALF_BOARD_SIZE + 1]) //  tuz position

	}
	get_legal_moves(player){
		return this.__generate_valid_moves(player)
	}
	has_legal_moves(){
		return count(this.get_legal_moves(1),1) != 0 || count(this.get_legal_moves(-1),1) != 0
	}
	is_win( player){
		// Победа в игре достигается двумя способами:

		// набор в свой казан 82 коргоола или более
		if (this.__players_scores[player] >= WIN_SCORE && this.__players_scores[-player] < WIN_SCORE)
			return true

		// ат сыроо (если после моего хода у противника не осталось ходов)
		// у противника не осталось ходов (см. ниже «ат сыроо») и при этом он ещё не набрал 81 коргоол
		if ( count(this.__generate_valid_moves(-player),1) == 0 && this.__players_scores[-player] < WIN_SCORE )
			return true

		return false
	}
	execute_move( move, player){
		let game_state = copy(this.__pieces)
		let balls_in_first_pit = game_state[move]
		let last_pit = move + balls_in_first_pit
		let last_pit_looped = last_pit < len(game_state) ? last_pit : last_pit % len(game_state)
		last_pit_looped -= 1
		if (last_pit_looped < 0)
			last_pit_looped = len(game_state) - 1

		if (balls_in_first_pit == 1){
			// Если в исходной лунке только один камень, то он перекладывается в следующую лунку.
			last_pit_looped += 1

			if (last_pit_looped >= len(game_state))
				last_pit_looped = 0

			game_state[move] = 0
			game_state[last_pit_looped] += balls_in_first_pit
		} else {
			// игрок берёт все камни из любой своей лунки «дом» и, начиная с этой же лунки, раскладывает их по одному против часовой стрелки в свои и чужие дома
			game_state[move] = 0
			for (let pit of range(move,last_pit)){
				if (pit >= len(game_state))
					pit = pit % len(game_state)
				game_state[pit] += 1
			}
		}


		// Если последний коргоол попадает в дом соперника и 
		// количество коргоолов в нём становится чётным, то коргоолы из этого дома переходят в казан игрока, совершившего ход.
		if  (
			this.__is_pit_dont_belongs_to_player(last_pit_looped,player) &&
			game_state[last_pit_looped] % 2 == 0
			){
			this.__players_scores[player] += game_state[last_pit_looped]
			game_state[last_pit_looped] = 0
		}

		let opponents_last_pit = player == 1 ? BOARD_SIZE - 1 : BOARD_SIZE / HEIGHT - 1
		let opponents_tuz = this.__players_tuz[-player]

		// Если при ходе игрока А последний коргоол попадает в дом игрока Б и в нём после этого оказывается три коргоола, то этот дом объявляется тузом игрока А 
		//  1) игрок не может завести себе туз в самом последнем (девятом) доме соперника,
		//  2) игрок не может завести себе туз в доме с таким же порядковым номером, который имеет лунка-туз соперника,
		//  3) каждый игрок в течение игры может завести себе только один туз.
		if (this.__is_pit_dont_belongs_to_player(last_pit_looped,player)	&&
			game_state[last_pit_looped]		== 3							&&
			last_pit_looped 				!= opponents_last_pit			&&  //  1)
			last_pit_looped 				!= opponents_tuz				&&  //  2)
			this.__players_tuz[player]		== null){							//  3)
			// Эти три коргоола попадают в казан игрока
			this.__players_scores[player] += game_state[last_pit_looped]
			game_state[last_pit_looped] = 0
			this.__players_tuz[player] = last_pit_looped
		}
		this.__pieces = game_state


		// Ат сыроо Если после хода игрока А все его дома оказываются пустыми (ход «91»), то он попадает в ситуацию «ат сыроо».
		// Игрок Б делает свой очередной ход. Если после его хода в дома игрока А не попадает ни одного коргоола, то в этой ситуации у игрока А нет ходов и игра заканчивается. Коргоолы из домов игрока Б переходят в казан игрока Б и производится подсчёт коргоолов в казанах.
		if (count(this.__generate_valid_moves(-player),1) == 0){
			for (const [i, piece] of this.__pieces.entries()){
				this.__players_scores[player] += piece
				this.__pieces[i] = 0
			}
		}

		return this.get_encoded_state()

	}

	__generate_valid_moves(player){
		let possible_moves = Array(this.action_size).fill(0)
		let game_state = this.__pieces
		for (let i of range(0,this.action_size)){
			if ((player * this.__canonical_player) == 1 && (i < BOARD_SIZE/2) ||  // playes 1 side
				(player * this.__canonical_player) == -1 && (i >= BOARD_SIZE/2))		// playes -1 side
				possible_moves[i] = game_state[i] > 0 ? 1 : 0 //  можно сделать ход, если лунке есть камни
		}
		
		if (this.__players_tuz[player] != null && this.__players_tuz[player] >= 0 && this.__players_tuz[player] < this.action_size) //  туз игрока
			possible_moves[this.__players_tuz[player]] = game_state[this.__players_tuz[player]] > 0  ? 1 : 0

		if (this.__players_tuz[-player] != null && this.__players_tuz[-player] >= 0 && this.__players_tuz[-player] < this.action_size)
			possible_moves[this.__players_tuz[-player]] = 0

		return possible_moves
	}
	__is_pit_dont_belongs_to_player(pit,player){
		let players_pit = null
		if ((player * this.__canonical_player) == 1)
			players_pit = range(0, int(this.__size / 2))
		else
			players_pit = range(int(this.__size / 2), this.__size)
		
		if (players_pit.includes(this.__players_tuz[-player]))
			removeFromArray(players_pit, this.__players_tuz[-player])
		if (this.__players_tuz[player] != null)
			players_pit.push(this.__players_tuz[player])
		return !players_pit.includes(pit)
	}

//for tests

	set_pieces(pieces){
		this.__pieces = copy(pieces)
	}

	get_pieces(){
		return copy(this.__pieces)
	}

	get_players_scores(){
		return copy(this.__players_scores)
	}

	get_players_tuz(){
		return copy(this.__players_tuz)
	}
	set_players_tuz(player,value){
		this.__players_tuz[player] = value
	}
}



// helpers
function generate_encoded_state(i_state){ // TODO: move to utils
	let state = copy(i_state)

	let pieces = state.slice(0,18)
	let mid = int((len(pieces) + 1) / 2)

	firstHalf = PIT_STATE_ENCODER(pieces.slice(0,mid),		[11,MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE])
	firstHalf[9] = SCORE_ENCODER(state[18],					MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
	firstHalf[10] = TUZ_ENCODER(state[20],					MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)

	secondHalf = PIT_STATE_ENCODER(pieces.slice(-mid),		[11,MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE])
	secondHalf[9] = SCORE_ENCODER(state[19],				MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)
	secondHalf[10] = TUZ_ENCODER(state[21],					MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE)

	secondHalf = operationWith2DArray(secondHalf, -1, "*")

	result = concatenate(firstHalf, secondHalf)

	return result
}


function parse_encoded_state(i_state){ // TODO: move to utils
	let state = copy(i_state)

	HALF_BOARD_SIZE = int(BOARD_SIZE/2)
	mid=int((len(state) + 1) / 2)
	firstHalf = state.slice(0,mid)
	secondHalf = state.slice(-mid)
	firstSum = 0
	secondSum = 0



	for (let onehot of firstHalf)
		firstSum += sum(onehot)

	for (let onehot of secondHalf)
		secondSum += sum(onehot)

	if (firstSum > 0 || secondSum < 0){ //  playe 1 in firstHalf
		//noop
	}else{ // player -1 in firstHalf
		[firstHalf,secondHalf] = [secondHalf,firstHalf]
	}

	secondHalf = operationWith2DArray(secondHalf,-1,"*") // at this point second half always contains negative numbers



	result =		PIT_STATE_DECODER(firstHalf.slice(0,HALF_BOARD_SIZE))
	result = result.concat(PIT_STATE_DECODER(secondHalf.slice(0,HALF_BOARD_SIZE)))

	result = result.concat(SCORE_DECODER(firstHalf[HALF_BOARD_SIZE]))
	result = result.concat(SCORE_DECODER(secondHalf[HALF_BOARD_SIZE]))
	result = result.concat(TUZ_DECODER(firstHalf[HALF_BOARD_SIZE + 1]))
	result = result.concat(TUZ_DECODER(secondHalf[HALF_BOARD_SIZE + 1]))
	return result
}
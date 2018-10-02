//import Board


class TKGame{
	getActionSize(){
		return BOARD_SIZE
	}

	getNextState(board, player, action){
		let b = new Board()
		b.set_encoded_state(board)
		b.execute_move(action, player)
		return [b.get_encoded_state(), -player]
	}

	getValidMoves(board, player){
		let b = new Board()
		b.set_encoded_state(board)
		return b.get_legal_moves(player)
	}

	getGameEnded(board, player){
		let b = new Board()
		b.set_encoded_state(board)
		if (b.is_win(player, player))
			return 1
		if (b.is_win(-player, player))
			return -1
		if (b.has_legal_moves())
			return 0
		return 1e-4
	}

	getCanonicalForm(board, player){
		if (player == 1)
			return board
		else
			return operationWith2DArray(board,-1,"*")
	}

	stringRepresentation(board){
		return board.toString()
	}
}
function launchTests() {
	let test = new TestTKLogic()
	test.launchTests()
}

class TestTKLogic{

	launchTests(){
		let tests = [
			this.test_get_legal_moves,
			this.test_has_legal_moves,
			this.test_is_win,
			this.test_execute_move,
			this.test_tuz,
			this.test_encoded_state,
			this.testCanonicalForm,
			this.testNNOutputs
		]
		for (let test of tests){
			console.log("%c testing " + test.name, 'color: green; font-weight: bold;')
			this.setUp()
			test.bind(this)()
			this.tearDown()
		}
		console.log("%c DONE ", 'color: green; font-weight: bold;')
	}
	setUp(){
		this.board = new Board()
	}
	tearDown(){
		this.board = null
	}
	assertEqual(obj1,obj2){
		let 
		str1 = str(obj1),
		str2 = str(obj2)
		if (str1 != str2){
			throw new Error().stack + "\n" + str1 + " != " + str2
		} else {
			// console.log(str1 + " == " + str2)
		}
	}

	test_get_legal_moves(){
		this.assertEqual(this.board.get_legal_moves(1), 	[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
		this.assertEqual(this.board.get_legal_moves(-1), 	[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1])
		
		this.board.execute_move(1,1)
		this.board.execute_move(1,1)
		this.assertEqual(this.board.get_legal_moves(1),		[1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])

		this.board.set_pieces([9, 9, 9, 9, 9, 9, 5, 9, 9,		9, 2, 9, 9, 9, 9, 9, 9, 9])
		this.board.execute_move(6,1)
		this.board.execute_move(7,1)
		this.assertEqual(this.board.get_legal_moves(1), 	[1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0])
	}

	test_has_legal_moves(){
		this.assertEqual(this.board.has_legal_moves(), 	true)
	}

	test_is_win(){
		let state = [9, 9, 9, 9, 9, 9, 9, 9, 9,		9, 9, 9, 9, 9, 9, 9, 9, 9,		WIN_SCORE - 1,1,		null,null]
		this.board.set_encoded_state(generate_encoded_state(state))
		this.assertEqual(this.board.is_win(1),		false)
		this.assertEqual(this.board.is_win(-1),		false)
		this.board.execute_move(1,1)
		this.assertEqual(this.board.is_win(1),		true)

		// у противника не осталось ходов 
		state = [0, 0, 0, 0, 3, 0, 0, 0, 1,		0, 0, 0, 2, 1, 3, 2, 15, 5,		70,70,		null,4]
		this.board.set_encoded_state(generate_encoded_state(state))
		this.board.execute_move(8,1)
		this.assertEqual(this.board.is_win(-1),		true)
		this.board.execute_move(12,-1)
		this.assertEqual(this.board.is_win(-1),		true)
	}

	test_execute_move(){
		this.assertEqual(parse_encoded_state(this.board.execute_move(0,1)),		[1, 10, 10, 10, 10, 10, 10, 10, 10,		9,  9, 9, 9, 9, 9, 9, 9, 9,				0, 0, null, null])
		this.setUp()
		this.assertEqual(parse_encoded_state(this.board.execute_move(1,1)),		[9, 1, 10, 10, 10, 10, 10, 10, 10,		0,  9, 9, 9, 9, 9, 9, 9, 9,				10, 0, null, null])
		this.setUp()
		this.assertEqual(parse_encoded_state(this.board.execute_move(9,-1)),	[9, 9, 9, 9, 9, 9, 9, 9, 9,				1, 10, 10, 10, 10, 10, 10, 10, 10,		0, 0, null, null])
		this.setUp()
		this.assertEqual(parse_encoded_state(this.board.execute_move(6,1)),		[9, 9, 9, 9, 9, 9, 1, 10, 10,			10, 10, 10, 10, 10, 0, 9, 9, 9,			10, 0, null, null])
		this.setUp()
		this.assertEqual(parse_encoded_state(this.board.execute_move(15,-1)),	[10, 10, 10, 10, 10, 0,  9, 9, 9,		9, 9, 9, 9, 9, 9, 1, 10, 10,	0, 10, null, null])
		
		this.assertEqual(parse_encoded_state(this.board.execute_move(0,1)),		[1, 11, 11, 11, 11, 1,  10, 10, 10,		0, 9, 9, 9, 9, 9, 1, 10, 10,	10, 10, null, null])
		
		this.board.set_encoded_state(generate_encoded_state( 					[9, 9, 9, 9, 9, 9, 9, 9, 9,				25, 9, 9, 9, 9, 9, 9, 9, 9,				0, 0, 	null, null]))
		this.assertEqual(parse_encoded_state(this.board.execute_move(9,-1)),	[10, 10, 10, 10, 10, 10, 10, 10, 10,	2, 11, 11, 11, 11, 11, 11, 10, 10,		0, 0, 	null, null])

		this.board.set_encoded_state(generate_encoded_state( 					[3, 9, 9, 0, 0, 0, 0, 0, 0,				0, 0, 0, 0, 0, 0, 0, 0, 0,				70, 20,	null, null]))
		this.assertEqual(parse_encoded_state(this.board.execute_move(0,1)),		[0, 0, 0, 0, 0, 0, 0, 0, 0,				0, 0, 0, 0, 0, 0, 0, 0, 0,				91, 20,	null, null])
		this.assertEqual(this.board.is_win(1),true)
	}

	test_tuz(){
		this.board.set_pieces([9, 9, 9, 9, 9, 9, 9, 10, 10,		9, 9, 9, 9, 9, 9, 9, 1, 2])
		
		this.assertEqual(parse_encoded_state(this.board.execute_move(8,1)),		[9, 9, 9, 9, 9, 9, 9, 10, 1,	10, 10, 10, 10, 10, 10, 10, 2, 3,		0, 0, 	null, null])
		this.assertEqual(this.board.get_legal_moves(1),							[1, 1, 1, 1, 1, 1, 1, 1, 1,		0, 0, 0, 0, 0, 0, 0, 0, 0])
		
		this.assertEqual(parse_encoded_state(this.board.execute_move(7,1)),		[9, 9, 9, 9, 9, 9, 9, 1, 2,		11, 11, 11, 11, 11, 11, 11, 0, 3,		3, 0, 	16, null])
		this.assertEqual(parse_encoded_state(this.board.execute_move(9,-1)),	[10, 0, 9, 9, 9, 9, 9, 1, 2,	1, 12, 12, 12, 12, 12, 12, 1, 4,		3, 10,	16, null])
		this.assertEqual(this.board.get_legal_moves(1),							[1, 0, 1, 1, 1, 1, 1, 1, 1,		0, 0, 0, 0, 0, 0, 0, 1, 0])

		this.setUp()
		this.board.set_pieces([1, 2, 4, 6, 20, 16, 13, 0, 1,	1, 2, 2, 1, 1, 7, 3, 2, 5])
		this.board.execute_move(0,1)
		this.assertEqual(this.board.get_players_tuz(),		{"1": null, "-1": null})

		this.setUp()
		this.board.set_pieces([1, 1, 2, 3, 1, 1, 8, 6, 15,	1, 2, 1, 16, 3, 4, 3, 1, 5])
		this.board.set_players_tuz(-1,1)
		this.assertEqual(this.board.get_legal_moves(-1),							[0, 1, 0, 0, 0, 0, 0, 0, 0,		1, 1, 1, 1, 1, 1, 1, 1, 1,])
		this.board.set_players_tuz(-1,0)
		this.assertEqual(this.board.get_legal_moves(-1),							[1, 0, 0, 0, 0, 0, 0, 0, 0,		1, 1, 1, 1, 1, 1, 1, 1, 1,])
	}


	test_encoded_state(){
		let state = 	[9, 9, 9, 9, 1, 9, 9, 9, 9,		9, 9, 9, 9, 9, 9, 9, 9, 9,		1,16,		1,null]
		
		let state1 = generate_encoded_state(state)
		this.board.set_encoded_state(state1)
		let state2 = this.board.get_encoded_state()
		state1 = str(state1)
		state2 = str(state2)
		this.assertEqual(state1,state2)

		// canonical -1
		this.setUp()
		state1 = operationWith2DArray(generate_encoded_state(state), -1, "*")
		this.board.set_encoded_state(state1)
		state2 = this.board.get_encoded_state()
		state1 = str(state1)
		state2 = str(state2)
		this.assertEqual(state1,state2)
	}

	//test tk game

	testCanonicalForm(){
		let game = new TKGame()
		let board = this.board.execute_move(0, 1)
		
		let canonical_form_p1 = game.getCanonicalForm(board, 1)
		let valids_p1 = game.getValidMoves(canonical_form_p1,1)
		this.assertEqual(valids_p1, [1, 1, 1, 1, 1, 1, 1, 1, 1,	0, 0, 0, 0, 0, 0, 0, 0, 0])


		let canonical_form_p2 = game.getCanonicalForm(board, -1)
		let valids_p2 = game.getValidMoves(canonical_form_p2,1)

		this.assertEqual(valids_p2, [0, 0, 0, 0, 0, 0, 0, 0, 0,	1, 1, 1, 1, 1, 1, 1, 1, 1])
	}

	testNNOutputs(){
		let n1 = new NNet()

		let game = new TKGame()
		let
		state = [9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 10, 10, 10, 10, 10, 10, 10, 10, 0, 0, null, null],
		encoded_state = generate_encoded_state(state),
		canonical_form = game.getCanonicalForm(encoded_state, -1)

		let prediction = n1.predict(canonical_form)
		let action = argmax(prediction[0])

		// print(canonical_form)
		// print(prediction)

		this.assertEqual(action,10)
	}
}
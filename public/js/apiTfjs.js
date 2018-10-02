const NUMBER_OF_MCTS_SIMULATIONS = 100

function importFromUrl(url){
	return new Promise((resolve, reject) => {
		let script = document.createElement('script')
		script.onload = resolve
		script.src = url
		document.body.appendChild(script);
	})
}

window.addEventListener("DOMContentLoaded", domContentLoaded);
function domContentLoaded() {
	console.log("Importing dependencies ...")
	importFromUrl("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@0.13.0")
	.then(() => {return importFromUrl("/js/tfjs/utils.js")})
	.then(() => {return importFromUrl("/js/tfjs/MCTS.js")})
	.then(() => {return importFromUrl("/js/tfjs/tk/keras/NNet.js")})
	.then(() => {return importFromUrl("/js/tfjs/TKLogick.js")})
	.then(() => {return importFromUrl("/js/tfjs/TKGame.js")})
	// .then(() => {return importFromUrl("/js/tfjs/tk/test/testTKLogick.js")}) // uncomment for tests
	// .then(() => {document.getElementById("pit0").addEventListener('click', launchTests, false); return new Promise((resolve,reject)=>{resolve()}) }) // uncomment for tests
	.then(() => {console.log("Dependencies imported"); setup()})
}

function setup(){
	document.getElementById("pit0").addEventListener('click', testPrediction, false)
}


function testPrediction(){

	const nnet = new NNet()
	if (!nnet.modelLoaded){
		return
	}

	const state = 	[9, 9, 9, 9, 1, 9, 9, 9, 9,		9, 9, 9, 9, 9, 9, 9, 9, 9,		1,16,		1,null]
	const board = new Board()
	board.set_encoded_state(generate_encoded_state(state))
	const encoded_state = board.get_encoded_state()

	const args = {
		numMCTSSims:NUMBER_OF_MCTS_SIMULATIONS,
		cpuct:1
	}



	const game = new TKGame()
	const mcts = new MCTS(game, nnet, args)
	console.log("MCTS predicting ...")
	const action = argmax(mcts.getActionProb(encoded_state, temp=0))
	console.log("MCTS predicting done")
	console.log(action)
}

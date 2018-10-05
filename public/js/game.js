const
WIDTH = 9,
HEIGHT = 2,
BOARD_SIZE = WIDTH * HEIGHT,
USER_PLAYER_ID = 1 //1 or -1

var boardState
var playersTuz
var playersScores
var player //current player id 1 or -1
var legalMoves

var loading = false

//UI
var pitDivs = []
var scoreDivs = []
var logsDiv = null
var loadingIndicator = null

//LifeCycle
window.addEventListener("DOMContentLoaded", domContentLoaded);

function domContentLoaded() {
	bindViews();
}

//ui utils
function bindViews() {
	for (var i in [...Array(BOARD_SIZE).keys()]) {
		pitDivs.push(document.getElementById("pit" + i));
		pitDivs[i].addEventListener('click', function(event) {
			if (loading){ return }
			showLoading()
			setTimeout(() => { executeAction(event.target.id.match(/\d+/g).map(Number)[0])},10)
		}, false);
	}
	for (var i in [...Array(2).keys()]) {
		scoreDivs.push(document.getElementById("score" + i));
	}
	logsDiv = document.getElementById("logsDiv")
	loadingIndicator = document.getElementById("loadingIndicator")
	
	showLoading()
	setupApi()
	.then(() => {
		reset()
		refresh()
	})
}

function refresh(isHideLoading=true){
	boardState.forEach(function (value, i) {
		pitDivs[i].innerHTML = value
	});

	playersScores.forEach(function (value, i) {
		scoreDivs[i].innerHTML = value
	});

	scoreDivs[0].className += " playerPit"
	scoreDivs[1].className += " enemyPit"

	var playerPits = Array(9).fill(true).concat(Array(9).fill(false))
	if (playersTuz[0] != null){
		playerPits[playersTuz[0]] = true
	}
	if (playersTuz[1] != null){
		playerPits[playersTuz[1]] = false
	}
	playerPits.forEach(function (value, i) {
		pitDivs[i].className = pitDivs[i].className.replace(" playerPit","")
		pitDivs[i].className = pitDivs[i].className.replace(" enemyPit","")
		if (value){
			pitDivs[i].className += " playerPit"
		} else {
			pitDivs[i].className += " enemyPit"
		}
		pitDivs[i].disabled = !legalMoves[i]
	});
	if (isHideLoading)
		hideLoading()
}

//game
function reset(){
	boardState = Array(BOARD_SIZE).fill(9) //0-8 player 1, 9-17 player -1
	playersTuz = Array(2).fill(null)//0 player 1, 1 player -1
	playersScores = Array(2).fill(0)
	player = 1 // 1 or -1
	legalMoves = Array(9).fill(true).concat(Array(9).fill(false))
}

function executeAction(actionId){

	var data = getStateData()
	data["action"] = actionId 
	logAction(actionId)
	getNextState(data)
	.then(function(json){
		if (json.winner != null){
			return showWinnerAlert(json.winner)
		}
		setStateData(json)
		refresh(false)
		return predictAction(getStateData())
	})
	.then(function(json){
		var data = getStateData()
		data["action"] = json.action
		logAction(json.action)
		return getNextState(data)
	})
	.then(function(json){
		if (json.winner != null){
			return showWinnerAlert(json.winner)
		}
		setStateData(json)
		refresh()
	})
	.catch(function(data) {
		if (data == "GAME_ENDED"){
			return
		}
		if (data instanceof Error ){
			throw data
		}
		log("Network error " + data.status,true)
		reset()
		refresh()
	})
}


function getStateData(){
	var data = {
		"board_state":boardState,
		"players_scores":playersScores,
		"players_tuz":playersTuz,
		"player":player
	}
	return data
}
function setStateData(json){
	player = json.next_player
	legalMoves = json.next_player_legal_moves
	playersScores = json.players_scores
	playersTuz = json.players_tuz
	boardState = json.state
}

//loading
function showLoading(){
	loading = true
	loadingIndicator.className = "loader"
}
function hideLoading(){
	loading = false
	loadingIndicator.className = 'hidden'
}

//alerts
function logAction(actionId){
	var actionId = actionId + 1
	if (player == USER_PLAYER_ID){
		log("Ваш ход:        " + actionId)
	} else {
		log("Ход противника: " + actionId)
	}
}
function showWinnerAlert(winner){
	if (winner == USER_PLAYER_ID){
		log("Вы победили",true)
	}
	if (winner == -USER_PLAYER_ID){
		log("Противник победил",true)
	}
	reset()
	refresh()
	return rejectPromise("GAME_ENDED")
}



//utils
function log(message,showAlert=false){
	// console.log(message)
	logsDiv.innerHTML = message + "<br>" + logsDiv.innerHTML
	if (showAlert){
		alert(message)
	}
}
function rejectPromise(reason){
	return new Promise(function(resolve, reject) {
		reject(reason)
	})
}
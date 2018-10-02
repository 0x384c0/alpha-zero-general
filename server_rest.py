import Arena
from MCTS import MCTS
from tk.TKGame import TKGame
from tk.TKLogic import BOARD_SIZE, Board
from tk.keras.NNet import NNetWrapper as NNet
from tk.test.testTKLogick import generate_encoded_state, parse_encoded_state

from flask import Flask, request, jsonify, send_from_directory
from utils import *


# model
n1p = None
def load_model():
	global n1p, g
	g = TKGame()
	n1 = NNet(g)
	n1.load_checkpoint('temp/','best.pth.tar')
	n1.nnet.model._make_predict_function() # workaround from https://github.com/keras-team/keras/issues/6462
	args1 = dotdict({'numMCTSSims': num_MCTS_sims(), 'cpuct':1.0})
	mcts1 = MCTS(g, n1, args1)
	n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

# utils
def validate(json):
	assert(len(json["board_state"]) == BOARD_SIZE)
	assert(len(json["players_scores"]) == 2)
	assert(len(json["players_tuz"]) == 2)
	assert(isinstance(json["board_state"][0], (int, float, complex)))
	assert(isinstance(json["players_scores"][0], (int, float, complex)))

def get_data(json):
	player = json["player"]

	state = json["board_state"]
	state += json["players_scores"]
	state += json["players_tuz"]
	return player, state


# api
app = Flask(__name__)

@app.route("/api/predict/",methods=['POST'])
def predict():
	# load_model()
	json = request.get_json()
	validate(json)
	player, state = get_data(json)
	

	encoded_state = generate_encoded_state(state)
	canonical_form = g.getCanonicalForm(encoded_state, player)

	action = int(n1p(canonical_form)) #np.int64 to int
	return jsonify({"action":action})


@app.route("/api/next_state/",methods=['POST'])
def next_state():
	json = request.get_json()
	validate(json)
	assert(isinstance(json["action"], (int, float, complex)))

	player, prev_state = get_data(json)
	action = json["action"]

	prev_encoded_state = generate_encoded_state(prev_state)
	board = Board()

	board.set_encoded_state(prev_encoded_state)
	board.execute_move(action, player)

	next_player = -player
	next_player_legal_moves = board.get_legal_moves(next_player)

	state = board.get_pieces()
	players_scores = board.get_players_scores()
	players_tuz = board.get_players_tuz()
	
	#np.int64 to int
	state = list(map(int, state))
	players_scores = {k: int(v) for k, v in players_scores.items()}
	players_tuz = {k: int(v) if v is not None else None  for k, v in players_tuz.items()}

	winner = None
	if board.is_win(1,player):
		winner = 1
	elif board.is_win(-1,player):
		winner = -1

	return jsonify({
		"next_player":next_player,
		"next_player_legal_moves":next_player_legal_moves,
		"state":state,
		"players_scores":[players_scores[1],players_scores[-1]],
		"players_tuz":[players_tuz[1],players_tuz[-1]],
		"winner":winner
		})

#TODO: use nginx for static files
public_dir = "public/"
@app.route('/')
def root():
    return send_from_directory(public_dir, "index.html")

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(public_dir + 'css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(public_dir + 'js', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory(public_dir + 'img', path)

# main
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load_model()
	app.run(host='0.0.0.0')
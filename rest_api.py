import Arena
from MCTS import MCTS
from tk.TKGame import TKGame
from tk.TKLogic import BOARD_SIZE
from tk.keras.NNet import NNetWrapper as NNet
from tk.test.testTKLogick import generate_encoded_state

from flask import Flask, request, jsonify
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

# api
app = Flask(__name__)

@app.route("/api/predict/",methods=['POST'])
def predict():
	# load_model()
	json = request.get_json()
	assert(len(json["board_state"]) == BOARD_SIZE)
	assert(len(json["players_scores"]) == 2)
	assert(len(json["players_tuz"]) == 2)
	assert(isinstance(json["board_state"][0], (int, float, complex)))
	assert(isinstance(json["players_scores"][0], (int, float, complex)))

	curPlayer = json["player"]

	state = json["board_state"]
	state += json["players_scores"]
	state += json["players_tuz"]
	

	board = generate_encoded_state(state)
	canonical_form = g.getCanonicalForm(board, curPlayer)

	# raise ValueError("\n board \n" + str(board) + "\n canonical_form \n " + str(canonical_form))

	action = int(n1p(canonical_form))
	return jsonify({"action":action})


# main
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load_model()
	app.run()
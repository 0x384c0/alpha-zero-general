
function getKey(stringRepresentation,action){
	return stringRepresentation + action
}

const EPS = 1e-8

class MCTS{
	constructor(game, nnet, args){
		this.game = game
		this.nnet = nnet
		this.args = args
		this.Qsa = {}		// stores Q values for s,a (as defined in the paper)
		this.Nsa = {}		// stores #times edge s,a was visited
		this.Ns = {}		// stores #times board s was visited
		this.Ps = {}		// stores initial policy (returned by neural net)

		this.Es = {}		// stores game.getGameEnded ended for board s
		this.Vs = {}		// stores game.getValidMoves for board s
	}

	getActionProb(canonicalBoard) {
		for (let i of range(this.args.numMCTSSims)){
			this.search(canonicalBoard)
		}
		let s = this.game.stringRepresentation(canonicalBoard)

		let counts = []
		for (let a of range(this.game.getActionSize())){
			if (getKey(s,a) in this.Nsa){
				counts.push(this.Nsa[getKey(s,a)])
			} else {
				counts.push(0)
			}
		}

		let bestA = argmax(counts)
		let probs = Array(len(counts)).fill(0)
		probs[bestA]=1
		return probs
	}

	search(canonicalBoard){
		const s = this.game.stringRepresentation(canonicalBoard)

		if (!(s in this.Es)){
			this.Es[s] = this.game.getGameEnded(canonicalBoard, 1)
		}
		if (this.Es[s]!=0){
			return -this.Es[s]
		}

		if (!(s in this.Ps)){
			let prediction = this.nnet.predict(canonicalBoard)
			this.Ps[s] = prediction[0]
			let v = prediction[1]
			let valids = this.game.getValidMoves(canonicalBoard, 1)
			this.Ps[s] = operationWithArrays(this.Ps[s],valids,"*")
			let sum_Ps_s = sum(this.Ps[s])
			if (sum_Ps_s > 0) {
				this.Ps[s] = operationWithArrays(this.Ps[s],sum_Ps_s,"/")
			} else {
				console.log("All valid moves were masked, do workaround.")
				this.Ps[s] = operationWithArrays(this.Ps[s],valids,"+")
				this.Ps[s] = operationWithArrays(this.Ps[s],sum(this.Ps[s]),"/")
			}
			this.Vs[s] = valids
			this.Ns[s] = 0
			return -v
		}

		let valids = this.Vs[s]
		let cur_best = -Number.MAX_VALUE
		let best_act = -1

		for (let a of range(this.game.getActionSize())){
			if (valids[a] != 0){
				let u = null
				if (getKey(s,a) in this.Qsa){
					u = this.Qsa[getKey(s,a)] + this.args.cpuct * this.Ps[s][a] * Math.sqrt(this.Ns[s]) / (1+this.Nsa[getKey(s,a)])
				} else {
					u = this.args.cpuct*this.Ps[s][a]*Math.sqrt(this.Ns[s] + EPS)	 // Q = 0 ?
				}
				if (u > cur_best){
					cur_best = u
					best_act = a
				}
			}
		}

		let a = best_act
		let nsArr = this.game.getNextState(canonicalBoard, 1, a)
		let next_s = nsArr[0]
		let next_player = nsArr[1]

		next_s = this.game.getCanonicalForm(next_s, next_player)

		let v = this.search(next_s)

		if (getKey(s,a) in this.Qsa){
			this.Qsa[getKey(s,a)] = (this.Nsa[getKey(s,a)]*this.Qsa[getKey(s,a)] + v)/(this.Nsa[getKey(s,a)]+1)
			this.Nsa[getKey(s,a)] = this.Nsa[getKey(s,a)] + 1
		} else {
			this.Qsa[getKey(s,a)] = v
			this.Nsa[getKey(s,a)] = 1
		}
		this.Ns[s] = this.Ns[s] + 1
		return -v
	}
}
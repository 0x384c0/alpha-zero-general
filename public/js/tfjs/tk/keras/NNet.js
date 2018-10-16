var _model = null
var _loading = false
class NNet{
	load(){
		if (_model == null && !_loading){
			_loading = true
			console.log("Loading model ... ")
			return  tf
			.loadModel('model/model.json')
			.then((i_model)=>{
				_model = i_model
				_loading = false
				console.log("Model loaded ")
				return Promise.resolve()
			})
		} else{
			return Promise.resolve()
		}
	}

	get modelLoaded(){
		return _model != null
	}

	predict(canonicalBoard){
		tf.nextFrame()
		return tf.tidy(() => {
			const xs = tf.tensor3d(
				[canonicalBoard],
				[1, 22, MAX_ARRAY_LEN_OF_ENCODED_PIT_STATE]
			)

			const prediction = _model.predict(xs)

			let actions = Array.from(prediction[0].dataSync())
			let winProbability = Array.from(prediction[1].dataSync())

			// print("predict")
			// print("board")
			// print(canonicalBoard)
			// print("action")
			// // xs.print()
			// // prediction[0].print()
			// prediction[1].print()
			// print(argmax(actions))


			return [actions,winProbability]
		})
	}
}
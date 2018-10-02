var model = null
var loading = false
class NNet{
	constructor(){
		if (model == null && !loading){
			loading = true
			console.log("Loading model ... ")
			tf.loadModel('/model/model.json')
			.then((i_model)=>{
				model = i_model
				loading = false
				console.log("Model loaded ")
			})
			.catch((error)=>{
				console.log("Loading model error: " + error)
			})
		}
	}

	get modelLoaded(){
		return model != null
	}

	predict(canonicalBoard){
		const xs = tf.tensor3d(
		[canonicalBoard],
		[1, 22, 8]
		)
		const prediction = model.predict(xs)
		let actions = Array.from(prediction[0].dataSync())
		let winProbability = Array.from(prediction[1].dataSync())
		return [actions,winProbability]
	}
}
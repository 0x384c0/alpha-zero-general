function importTfjs(){
	var script = document.createElement('script')
	script.src = "https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@0.13.0"
	document.body.appendChild(script);
}

window.addEventListener("DOMContentLoaded", domContentLoaded);
function domContentLoaded() {
	importTfjs()
	document.getElementById("pit0").addEventListener('click', test, false);
}



async function test() {
	const model = await tf.loadModel('/model/model.json');
	const xs = tf.tensor3d(
		[[[ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.],
		[ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.],
		[ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.],
		[ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.],
		[ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.],
		[ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.],
		[ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.],
		[ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.],
		[ 0.,  0.,  0.,  0.,  1.,  0.,  0.,  1.],
		[ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
		[ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
		[-0., -0., -0., -0., -1., -0., -0., -1.],
		[-0., -0., -0., -0., -1., -0., -0., -1.],
		[-0., -0., -0., -0., -1., -0., -0., -1.],
		[-0., -0., -0., -0., -1., -0., -0., -1.],
		[-0., -0., -0., -0., -1., -0., -0., -1.],
		[-0., -0., -0., -0., -1., -0., -0., -1.],
		[-0., -0., -0., -0., -1., -0., -0., -1.],
		[-0., -0., -0., -0., -1., -0., -0., -1.],
		[-0., -0., -0., -0., -1., -0., -0., -1.],
		[-0., -0., -0., -0., -0., -0., -0., -0.],
		[-1., -1., -1., -1., -1., -1., -1., -1.],]],
		[1, 22, 8]);
	const prediction = model.predict(xs)
	prediction[0].print()
 	prediction[1].print()

}
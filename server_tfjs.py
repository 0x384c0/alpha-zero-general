from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#TODO: use nginx for static files
public_dir = "public/"
@app.route('/')
def root():
	return send_from_directory(public_dir, "index.html")

@app.route('/css/<path:path>')
def send_css(path):
	return send_from_directory(public_dir + 'css', path)

@app.route('/img/<path:path>')
def send_img(path):
	return send_from_directory(public_dir + 'img', path)

@app.route('/js/<path:path>')
def send_js(path):
	return send_from_directory(public_dir + 'js', path)

@app.route('/js/api.js') # api.js
def send_js_api():
	return send_from_directory(public_dir + 'js', "apiTfjs.js")

@app.route('/model/<path:path>')
@cross_origin()
def send_model(path):
	return send_from_directory('temp/tfjs', path)


# main
if __name__ == "__main__":
	app.run(host='0.0.0.0')
PYTHON=python
GPU_MODE="True" # run "make setup-gpu" before setting to True
NUMBER_OF_TRAIN_ITERATIONS=1000
NUMBER_OF_MCTS_SIMULATIONS=100

all:
	$(MAKE) docker_build
	$(MAKE) docker_start

# utils
setup:
	pip install -r requirements.txt


setup-gpu:
	pip uninstall tensorflow
	pip install tensorflow-gpu
	pip install -r requirements.txt
	echo "Now set GPU_MODE to \"True\" in MakeFile"

clean:
	rm -rf temp

test:
	export DEBUG_MODE="True"; \
	$(PYTHON) -m tk.test.testTKLogick; \
	$(PYTHON) -m tk.test.testTKGame; \
	$(PYTHON) -m tk.test.testNNet

# nn
train:
	export NUMBER_OF_TRAIN_ITERATIONS=$(NUMBER_OF_TRAIN_ITERATIONS); \
	export NUMBER_OF_MCTS_SIMULATIONS=$(NUMBER_OF_MCTS_SIMULATIONS); \
	export GPU_MODE=$(GPU_MODE); \
	$(PYTHON) train_with_alpha_zero.py

train_with_heuristic:
	export NUMBER_OF_TRAIN_ITERATIONS=$(NUMBER_OF_TRAIN_ITERATIONS); \
	$(PYTHON) train_with_heuristic.py

cpulimit:
	sleep 1 && cpulimit -p $$(pgrep "Python") -l 200

play:
	export DEBUG_MODE="True"; \
	export NUMBER_OF_MCTS_SIMULATIONS=$(NUMBER_OF_MCTS_SIMULATIONS); \
	export GPU_MODE=$(GPU_MODE); \
	$(PYTHON) pit.py

play_with_himan:
	export PLAY_WITH_HUMAN="True"; \
	export NUMBER_OF_MCTS_SIMULATIONS=$(NUMBER_OF_MCTS_SIMULATIONS); \
	export GPU_MODE=$(GPU_MODE); \
	$(PYTHON) pit.py

#TensorFlow.js
generate_tfjs_model_from_keras:
	rm -rf temp/tfjs/
	python keras_model_to_tfjs.py
	tensorflowjs_converter --input_format keras "temp/best.h5" temp/tfjs

generate_static_tfjs_site:
	if [ ! -d "temp/tfjs" ]; then echo "first run \"make generate_tfjs_model_from_keras\""; exit 1; fi;
	rm -rf temp/public
	cp -r public temp/
	rm temp/public/js/apiRest.js
	mv temp/public/js/apiTfjs.js temp/public/js/api.js
	cp -r temp/tfjs temp/public
	mv temp/public/tfjs temp/public/model
	echo "temp/public is ready for hosting"

start_server_tfjs:
	$(PYTHON)  server_tfjs.py

# server rest api
start_server_rest:
	export NUMBER_OF_MCTS_SIMULATIONS=$(NUMBER_OF_MCTS_SIMULATIONS); \
	$(PYTHON)  server_rest.py

test_server:
	curl --header "Content-Type: application/json" \
	--request POST \
	--data '{"board_state": [9, 9, 9, 9, 9, 9, 9, 9, 9,    9, 9, 9, 9, 9, 9, 9, 9, 9], "players_scores":[0, 0], "players_tuz":[null,null], "player":1}' \
	"http://localhost:5000/api/predict/"

	curl --header "Content-Type: application/json" \
	--request POST \
	--data '{"board_state": [9, 9, 9, 9, 9, 9, 9, 9, 9,    9, 9, 9, 9, 9, 9, 9, 9, 9], "players_scores":[0, 0], "players_tuz":[null,null], "player":1, "action":2}' \
	"http://localhost:5000/api/next_state/"

# docker
IMAGE_TAG="alpha_zero_general"
CONTAINER_NAME="alpha_zero_general_5000"
docker_build:
	docker rm $(CONTAINER_NAME) || true
	docker rmi --no-prune $(IMAGE_TAG) || true
	docker build -t $(IMAGE_TAG)  --build-arg CACHEBUST=$$(date +%s) .
	docker create  -it -p 5000:5000 --name $(CONTAINER_NAME) $(IMAGE_TAG)

docker_start:
	docker start -ai $(CONTAINER_NAME)

docker_start_windows:
	winpty docker start -ai $(CONTAINER_NAME)
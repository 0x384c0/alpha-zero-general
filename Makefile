PYTHON=python
GPU_MODE="True" # run "make setup-gpu" before setting to True
NUMBER_OF_TRAIN_ITERATIONS=1
NUMBER_OF_MCTS_SIMULATIONS=100

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
	cd tk && $(PYTHON) -m test.testTKLogick
	$(PYTHON) -m tk.test.testTKGame

train:
	export NUMBER_OF_TRAIN_ITERATIONS=$(NUMBER_OF_TRAIN_ITERATIONS); \
	export NUMBER_OF_MCTS_SIMULATIONS=$(NUMBER_OF_MCTS_SIMULATIONS); \
	export GPU_MODE=$(GPU_MODE); \
	$(PYTHON) main.py

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
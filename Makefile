PYTHON=python3
GPU_MODE="False" # run "make setup-gpu" before setting to True
NUMBER_OF_TRAIN_ITERATIONS=1

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
	export GPU_MODE=$(GPU_MODE); \
	$(PYTHON) main.py

play:
	export GPU_MODE=$(GPU_MODE); \
	$(PYTHON) pit.py

play_with_himan:
	export GPU_MODE=$(GPU_MODE); \
	export PLAY_WITH_HUMAN="True"; \
	$(PYTHON) pit.py
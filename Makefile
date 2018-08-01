PYTHON=python3

setup:
	pip install -r requirements.txt

clean:
	rm -rf temp

test:
	export DEBUG_MODE="True"; \
	cd tk && $(PYTHON) -m test.testTKLogick
	$(PYTHON) -m tk.test.testTKGame

train:
	$(PYTHON) main.py

play:
	$(PYTHON) pit.py
	# export DEBUG_MODE="True"; \
	# $(PYTHON) pit.py
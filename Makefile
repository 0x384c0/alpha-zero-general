PYTHON=python3

clean:
	rm -rf temp

test:
	export DEBUG_MODE="True"; \
	cd tk && $(PYTHON) -m test.testTKLogick
	$(PYTHON) -m tk.test.testTKGame

train:
	$(PYTHON) main.py

play:
	export DEBUG_MODE="True"; \
	$(PYTHON) pit.py
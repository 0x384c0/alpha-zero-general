PYTHON=python3

test:
	cd tk && $(PYTHON) -m test.testTKLogick

run:
	$(PYTHON) main.py

play:
	$(PYTHON) pit.py
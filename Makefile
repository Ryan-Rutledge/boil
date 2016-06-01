all:
	python3 prepare.py
test:
	python3 -m unittest -v tests.test

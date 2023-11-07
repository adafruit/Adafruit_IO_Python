publish: clean build
	twine upload dist/*

clean:
	#rm -rf Adafruit_BBIO.* build dist
	rm -f *.pyo
	rm -f *.egg
tests:
	py.test

build:
	python -m build

install: build
	pip install .
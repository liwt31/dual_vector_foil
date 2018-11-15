.PHONY: format debug test build clean

format:
	black .

debug:
	python -m pytest --pdb -s

test:
	python -m pytest --cov=dvf --cov-report=html --cov-report=term

build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist/

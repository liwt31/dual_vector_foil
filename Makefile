.PHONY: format test build clean

format:
	black .

test:
	python -m pytest

build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist/

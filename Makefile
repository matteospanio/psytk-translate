PYTHON := uv run python
all: dist/quiz.en.psytk dist/quiz.it.psytk dist/quiz.es.psytk

dist:
	mkdir -p dist

dist/quiz.en.psytk: dist
	$(PYTHON) main.py -l en -o $@

dist/quiz.it.psytk: dist
	$(PYTHON) main.py -l it -o $@

dist/quiz.es.psytk: dist
	$(PYTHON) main.py -l es -o $@

.PHONY: dist
clean:
	rm -rf dist

TEMPLATE := templates/quiz.psytk.jinja2
SRC := main.py
PYTHON := uv run python
OUTDIR := dist

LANG_FILES := $(wildcard languages/*.yml)
LANGS := $(basename $(notdir $(LANG_FILES)))

OUTFILES := $(foreach lang,$(LANGS),$(OUTDIR)/quiz.$(lang).psytk)

all: $(OUTFILES)

$(OUTDIR):
	mkdir -p $@

$(OUTDIR)/quiz.%.psytk: $(OUTDIR) $(TEMPLATE) $(SRC)
	$(PYTHON) $(SRC) -l $* -o $@

.PHONY: all clean
clean:
	rm -rf $(OUTDIR)

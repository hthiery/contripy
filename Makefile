O ?= output
o := $(O)/

all: $(o)contribution.html $(o)contribution.pdf


.PHONY: $(o)outfile.json
$(o)outfile.json: config.yaml
	./contripy --from 2010-01-01 -c config.yaml -o $@

$(o)index.adoc: $(o)outfile.json
	mkdir -p $(o)
	./report -i $< -d $(o) -o $(notdir $@)

$(o)contribution.html: $(o)index.adoc
	asciidoctor $< -o $@

$(o)contribution.pdf: $(o)index.adoc
	asciidoctor-pdf $< -o $@

clean:
	rm -f $(o)index.pdf
	rm -f $(o)index.html

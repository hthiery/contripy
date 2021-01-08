O ?= output
o := $(O)/

all: $(o)contribution.html $(o)contribution.pdf


.PHONY: $(o)outfile.json
$(o)outfile.json: contripy.cfg
	./contripy --from 2010-01-01 -c contripy.cfg -o $@

$(o)logo.png: images/contripy_logo.png
	cp images/contripy_logo.png $@

$(o)index.adoc: $(o)outfile.json $(o)logo.png
	mkdir -p $(o)
	./report -i $< -d $(o)

$(o)contribution.html: $(o)index.adoc
	asciidoctor $< -o $@

$(o)contribution.pdf: $(o)index.adoc
	asciidoctor-pdf $< -o $@

clean:
	rm -f $(o)index.pdf
	rm -f $(o)index.html

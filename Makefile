O ?= output
o := $(O)/

all: $(o)index.html $(o)index.pdf


$(o)outfile.json: config.yaml
	./contripy -c config.yaml -o $@

$(o)index.adoc: $(o)outfile.json
	mkdir -p $(o)
	./report -i $< -d $(o) -o $(notdir $@)

$(o)index.html: $(o)index.adoc
	asciidoctor $(o)index.adoc

$(o)index.pdf: $(o)index.adoc
	asciidoctor-pdf $(o)index.adoc

clean:
	rm -f $(o)index.pdf
	rm -f $(o)index.html

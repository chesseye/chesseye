OCAMLBUILD= ocamlbuild \
		-no-links -classic-display \
		-libs str \
		-tags debug,annot

MAIN=ochess
TARGET=native

all: $(MAIN)

$(MAIN): $(MAIN).$(TARET)
	cp _build/$(MAIN).$(TARGET) $(MAIN)

$(MAIN).$(TARET):
	$(OCAMLBUILD) $(MAIN).$(TARGET)


clean:
	ocamlbuild -clean

realclean: clean
	rm -f *~ $(MAIN)

cleanall: realclean

OCAMLBUILD= ocamlbuild \
		-no-links -classic-display \
		-libs str \
		-tags debug,annot

MAIN=ochess
MAINSIM=simul
TARGET=native

all: $(MAIN) $(MAINSIM)

$(MAIN): $(MAIN).$(TARGET)
	cp _build/$(MAIN).$(TARGET) $(MAIN)

$(MAINSIM): $(MAINSIM).$(TARGET)
	cp _build/$(MAINSIM).$(TARGET) $(MAINSIM)

$(MAIN).$(TARGET):
	$(OCAMLBUILD) $(MAIN).$(TARGET)

$(MAINSIM).$(TARGET):
	$(OCAMLBUILD) $(MAINSIM).$(TARGET)


clean:
	ocamlbuild -clean

realclean: clean
	rm -f *~ $(MAIN)

cleanall: realclean

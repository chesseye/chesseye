OCAMLBUILD= ocamlbuild \
		-no-links -classic-display \
		-libs str,unix \
		-tags debug,annot,thread

RMLBUILD= rmlbuild \
		-no-links -classic-display \
		-libs str \
		-tags debug,annot,thread

TARGET=native

all: controller ochess simul slowdown

controller: controller.rml.$(TARGET)
	cp _build/controller.rml.$(TARGET) controller

ochess: ochess.$(TARGET)
	cp _build/ochess.$(TARGET) ochess

simul: simul.$(TARGET)
	cp _build/simul.$(TARGET) simul

slowdown: slowdown.$(TARGET)
	cp _build/slowdown.$(TARGET) slowdown

controller.rml.$(TARGET):
	$(RMLBUILD) controller.rml.$(TARGET)


ochess.$(TARGET):
	$(OCAMLBUILD) ochess.$(TARGET)

simul.$(TARGET):
	$(OCAMLBUILD) simul.$(TARGET)

slowdown.$(TARGET):
	$(OCAMLBUILD) slowdown.$(TARGET)


clean:
	ocamlbuild -clean

realclean: clean
	rm -f *~ ochess simul

cleanall: realclean

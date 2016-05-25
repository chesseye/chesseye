.PHONY: all controller clean test

all: controller

controller: 
	(cd controller; make)

test:
	(cd cam; python -m unittest -v test)

clean:
	(cd controller; make clean)
	find . -name '*.pyc' -delete

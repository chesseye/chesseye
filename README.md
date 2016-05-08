# Readme

## Prerequisites

  * Python with OpenCV (tested with 3.1.0)
  * OCaml
  * [ReactiveML](http://reactiveml.org) (`opam install rml`)

## Compile

  * `cd controller; make`


## Run

  * To read data from the second camera (e.g. USB webcam on a laptop), and have the computer suggest moves for the black player, run: `python cam/chesseye.py --src=1 | controller/controller -kibbitz 1 | python voice/speak.py`

# Readme

This is the repository of the [ChessEye project, made at Techcrunch Disrupt 2016](http://devpost.com/software/chesseye).
A one minute presentation video is [available](https://youtu.be/bYtGw61YLRk).

## Prerequisites
  * Python with OpenCV (tested with 3.1.0)
  * OCaml
  * [ReactiveML](http://reactiveml.org) (`opam install rml`)
  * ChessEye has been tested on MacOSX and Ubuntu.

## Compile
  * `(cd controller; make)`

## Run
  * To read data from the second camera (e.g. USB webcam on a laptop), and have the computer suggest moves for black, run: `python cam/chesseye.py --src=1 | controller/controller -kibbitz 1 | python voice/speak.py`
  * To transcribe a video of a game to PGN, run `python cam/chesseye.py --src=game.mov --no-ui | controller/controller -kibbitz 0 | python export/pgn.py`

When operating from a file, you can also run the processes independently and save intermediary outputs to a file (it's just pipes after all).

## Current limitations
  * Promotion always promotes to queen
  * Board needs to occupy the majority of the frame and be relatively well aligned with the horizontal/vertical axes.
  * White needs to be "on the right" of the frame.


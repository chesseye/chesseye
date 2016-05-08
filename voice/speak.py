import os
import chess
import sys
import subprocess

import watson

def say(text):
    if watson.load_credentials() != None:
        if not os.environ["WAV_PLAYER"]:
            sys.stderr.write("You need to define the environment variable WAV_PLAYER.\n")
            sys.exit(1)
        wav_file = watson.get_file(text)
        subprocess.call([ os.environ["WAV_PLAYER"], wav_file ])
    else:
        subprocess.call([ "say", text ])

def say_fen_move(fen_str, uci_str):
    board = chess.Board(fen_str)
    move = board.parse_uci(uci_str)
    say(board.san(move))

def say_move(move_str):
    say(move_str)

if __name__ == "__main__":
    # Sometimes you make no sense, Python.
    for line in iter(sys.stdin.readline, ""):
        line = line[:-1]

        print "%s" % line

        verb = line[0:4]
        rest = line[5:]

        if verb == "MOVD":
            say("Move registered.")
        elif verb == "KIBB":
            say("I would play: %s" % rest)
        elif verb == "REST":
            say("The board was reset.")



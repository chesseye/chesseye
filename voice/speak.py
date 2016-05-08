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

    if len(sys.argv) < 2:
        sys.stderr.write("Expected command.\n")
        sys.exit(1)

    verb = sys.argv[1]

    if verb == "MOVD":
        say("Move registered.")
    elif verb == "KIBB":
        say("I would play: %s" % sys.argv[2])
    elif verb == "FENM":
        say_fen_move(sys.argv[2], sys.argv[3])
    else:
        sys.stderr.write("Unrecognized command: '%s'.\n" % verb)
        sys.exit(1)


import os
import chess
import sys
import subprocess
import re

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

def pronounce_move(fen_str, uci_str):
    board = chess.Board(fen_str)
    move = board.parse_uci(uci_str)

    san = board.san(move)

    if move == "O-O" or move == "o-o" or move == "0-0":
        return "king-side castle"
    elif move == "O-O-O" or move == "o-o-o" or move == "0-0-0":
        return "queen-side castle"
    
    s = " ".join(san)

    s = s.replace("K", "king")
    s = s.replace("Q", "queen")
    s = s.replace("R", "rook")
    s = s.replace("B", "bishop")
    s = s.replace("N", "knight")
    s = s.replace("x", "takes")
    s = s.replace("+", "check!")

    return s

def pronounce_uci(move):
    if move == "O-O" or move == "o-o" or move == "0-0":
        return "king-side castle"
    elif move == "O-O-O" or move == "o-o-o" or move == "0-0-0":
        return "queen-side castle"
    else:
        return " ".join(move)

if __name__ == "__main__":
    # Sometimes you make no sense, Python.
    for line in iter(sys.stdin.readline, ""):
        line = line[:-1]

        print "%s" % line

        verb = line[0:4]
        rest = line[5:]

        if verb == "MOVD":
            say("Move registered.")
            m = re.match("""^("[^"]*") ("[^"]*")$""", rest)
            if m is not None:
                say(pronounce_move(m.group(1)[1:-1], m.group(2)[1:-1]))

        elif verb == "KIBB":
            say("I would play: %s" % pronounce_uci(rest))
        elif verb == "REST":
            say("The board was reset.")



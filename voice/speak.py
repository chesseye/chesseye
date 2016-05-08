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
    if uci_str == "O-O" or uci_str == "o-o" or uci_str == "0-0":
        return "king-side castle"
    elif uci_str == "O-O-O" or uci_str == "o-o-o" or uci_str == "0-0-0":
        return "queen-side castle"

    board = chess.Board(fen_str)
    move = board.parse_uci(uci_str)

    san = board.san(move)
    
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
    # Fights the stuttering controller.
    last_was_rest = False

    # Sometimes you make no sense, Python.
    for line in iter(sys.stdin.readline, ""):
        try:
            line = line[:-1]

            print "%s" % line

            verb = line[0:4]
            rest = line[5:]

            if verb == "MOVD" and not last_was_rest:
                say("Move registered.")
                # m = re.match("""^("[^"]*") ("[^"]*")$""", rest)
                # if m is not None:
                #     say(pronounce_move(m.group(1)[1:-1], m.group(2)[1:-1]))

            elif verb == "KIBB":
                m = re.match("""^("[^"]*") ("[^"]*")$""", rest)
                if m is not None:
                    move_str = pronounce_move(m.group(1)[1:-1], m.group(2)[1:-1])
                else:
                    move_str = rest
                say("I would play: %s" % move_str)

            elif verb == "REST" and not last_was_rest:
                say("The board was reset.")
            elif verb == "ENDG":
                say(rest)

            if verb == "REST":
                last_was_rest = True
            else:
                last_was_rest = False
        except:
            print "There was an exception."


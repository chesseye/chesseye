import chess
import sys
import subprocess

def say(text):
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

    if verb == "MOVE":
        say_move(sys.argv[2])
    elif verb == "FENM":
        say_fen_move(sys.argv[2], sys.argv[3])
    else:
        sys.stderr.write("Unrecognized command: '%s'.\n" % verb)
        sys.exit(1)


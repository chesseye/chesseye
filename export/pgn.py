import datetime
import os
import chess
import chess.pgn
import sys
import subprocess
import re

board = chess.Board()

def make_move(fen_str, uci_str):
    # print "A: %s" % board.fen()
    # print "B: %s" % fen_str
    # print "U: %s" % uci_str
    # print ""

    # even castling should be represented as a (king) move
    if uci_str == "O-O" or uci_str == "o-o" or uci_str == "0-0":
        uci_str = "e1g1" if board.turn == chess.WHITE else "e8g8"
    elif uci_str == "O-O-O" or uci_str == "o-o-o" or uci_str == "0-0-0":
        uci_str = "e1c1" if board.turn == chess.WHITE else "e8c8"

    # TODO check that fen matches current board?
    move = board.parse_uci(uci_str)
    board.push(move)
    return

if __name__ == "__main__":
    for line in iter(sys.stdin.readline, ""):
        # try:
            line = line[:-1]

            verb = line[0:4]
            rest = line[5:]

            if verb == "MOVD" and not last_was_rest:
                m = re.match("""^("[^"]*") ("[^"]*")$""", rest)
                fen = m.group(1)[1:-1]
                uci = m.group(2)[1:-1]
                make_move(fen, uci)
            elif verb == "REST" and not last_was_rest:
                board.reset()
            elif verb == "ENDG":
                game = chess.pgn.Game.from_board(board)
                game.headers["Date"] = datetime.datetime.today().strftime("%Y.%m.%d")
                game.headers["Annotator"] = "ChessEye (https://github.com/chesseye)"
                print game

            if verb == "REST":
                last_was_rest = True
            else:
                last_was_rest = False
        # except:
        #     print "There was an exception."


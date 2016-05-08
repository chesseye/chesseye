#!/usr/bin/env python
import sys
import subprocess

def say_move(move_str):
    subprocess.call([ "say", move_str ])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Expected command.\n")
        sys.exit(1)

    verb = sys.argv[1]

    if verb == "MOVE":
        say_move(sys.argv[2])
    else:
        sys.stderr.write("Unrecognized command: '%s'.\n" % verb)
        sys.exit(1)


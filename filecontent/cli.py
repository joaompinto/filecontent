import sys
from optparse import OptionParser


def parse_cmd_line():
    parser = OptionParser()
    options, args = parser.parse_args()
    if len(args) < 1:
        print("Usage: {} url".format(sys.argv[0]))
        exit(1)
    return options, args


def main():
    options, args = parse_cmd_line()
    filename = args[0]
    print(filename)

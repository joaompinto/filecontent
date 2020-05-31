import sys
from optparse import OptionParser
from .fetcher import Fetcher
from pprint import pprint


def parse_cmd_line():
    parser = OptionParser()
    options, args = parser.parse_args()
    if len(args) < 1:
        print("Usage: {} url".format(sys.argv[0]))
        exit(1)
    return options, args


def main():
    options, args = parse_cmd_line()
    url = args[0]
    print("Getting content summary")
    fetcher = Fetcher(url)
    summary = fetcher.get_content()

    pprint(summary)
    # print(dumps(summary, indent=2))

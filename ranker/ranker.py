#!/usr/bin/env python3
"""
CLI application that parses match result inputs
and returns the rankings for the league.
"""

import argparse
import sys
import traceback

from pathlib import Path


def init_argparser(args):
    """
    Parse commandline arguments.
    """
    parser = argparse.ArgumentParser(
        description="Parse match results file/input and "
                    "compile rankings for the league.")
    parser.add_argument("results_file", default="",
                        help="path to file that contains match results")
    parser.add_argument("-v", "--version", action="version", version="0.0.1")

    return parser.parse_args(args)


def load_results_from_file(file_path):
    results_file = Path(file_path)

    if not results_file.exists():
        raise FileNotFoundError(
            f"The specified file [ {file_path} ] could not be found.")

    with open(results_file) as rf:
        results = rf.readlines()

    return results


def main():
    args = init_argparser(sys.argv[1:])

    try:
        results = load_results_from_file(args.results_file)
        print(results)
    except Exception as e:
        if isinstance(e, (FileNotFoundError)):
            print(e)
        else:
            print(f"Unidentified error: [ {e} ]")
            print(" - Please send traceback to developer:")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()

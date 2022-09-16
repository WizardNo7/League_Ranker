#!/usr/bin/env python3
"""
CLI application that parses match result inputs
and returns the rankings for the league.
"""

import traceback

from pathlib import Path


def load_results_from_file(file_path):
    results_file = Path(file_path)

    if not results_file.exists():
        raise FileNotFoundError(
            f"The specified file [ {file_path} ] could not be found.")

    with open(results_file) as rf:
        results = rf.readlines()

    return results


def main():
    try:
        results = load_results_from_file("test_file.txt")
    except Exception as e:
        if isinstance(e, (FileNotFoundError)):
            print(e)
        else:
            print(f"Unidentified error: [ {e} ]")
            print(" - Please send traceback to developer:")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()

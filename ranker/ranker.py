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


def parse_results(results):
    result_table = {}
    team_stats = {
        "wins": 0,
        "losses": 0,
        "draws": 0
    }

    for match in results:
        teams = match.strip().split(", ")

        for i in range(2):
            teams[i] = teams[i].rsplit(" ", 1)

            if teams[i][0] not in result_table:
                result_table[teams[i][0]] = team_stats.copy()

        if teams[0][1] < teams[1][1]:
            result_table[teams[0][0]]["losses"] += 1
            result_table[teams[1][0]]["wins"] += 1
        elif teams[0][1] > teams[1][1]:
            result_table[teams[0][0]]["wins"] += 1
            result_table[teams[1][0]]["losses"] += 1
        else:
            result_table[teams[0][0]]["draws"] += 1
            result_table[teams[1][0]]["draws"] += 1

    return result_table


def calculate_points(parsed_results):
    scored_results = {}

    for key in parsed_results:
        points = (3 * parsed_results[key]["wins"]
                  ) + parsed_results[key]["draws"]

        if points not in scored_results:
            scored_results[points] = []

        scored_results[points].append(key)

    return scored_results


def main():
    args = init_argparser(sys.argv[1:])

    try:
        results = load_results_from_file(args.results_file)
        parsed_results = parse_results(results)
        scored_results = calculate_points(parsed_results)
        print(scored_results)
    except Exception as e:
        if isinstance(e, (FileNotFoundError)):
            print(e)
        else:
            print(f"Unidentified error: [ {e} ]")
            print(" - Please send traceback to developer:")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()

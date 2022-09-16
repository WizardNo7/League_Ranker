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
        description="Parse match results file and "
                    "compile rankings for the league.")
    parser.add_argument("results_file", default="",
                        help="Path to file that contains match results")
    parser.add_argument("-o", "--output", default="",
                        help="File to use for ranking output. "
                        "Rankings will be printed if no file is specified.")
    parser.add_argument("-t", "--table", action="store_true", default=False,
                        help="Show the results as a table. "
                        "Rankings will be printed if no file is specified.")
    parser.add_argument("-v", "--version", action="version", version="0.0.1")

    return parser.parse_args(args)


def load_results_from_file(file_path):
    """Take file path, load results from file and into a list."""
    results_file = Path(file_path)

    if not results_file.exists():
        raise FileNotFoundError(
            f"The specified file [ {file_path} ] could not be found.")

    with open(results_file) as rf:
        results = rf.readlines()

    return results


def parse_results(results):
    """Take list of results, and compute team statistics into a dict."""
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
    """Take statistics dictionary and compile dict of teams per point total."""
    scored_results = {}

    for key in parsed_results:
        points = (3 * parsed_results[key]["wins"]
                  ) + parsed_results[key]["draws"]

        if points not in scored_results:
            scored_results[points] = []

        scored_results[points].append(key)

    return scored_results


def format_rankings(scored_results):
    """Take dict of teams per point, and format them into list for printing."""
    rankings = []

    place = 1
    for points in (sorted(scored_results, reverse=True)):
        suffix = ""
        if points != 1:
            suffix = "s"

        if len(scored_results[points]) > 1:
            for team in sorted(scored_results[points]):
                rankings.append(f"{place}. {team}, {points} pt{suffix}")
            place += len(scored_results[points])
        else:
            rankings.append(
                f"{place}. {scored_results[points][0]}, {points} pt{suffix}")
            place += 1

    return rankings


def output_rankings(rankings, output_file, output_table):
    """Take list of rankings and output as requested; stdout, file or table."""
    if output_file:
        rankings_file = Path(output_file)

        with rankings_file.open(mode="w") as rf:
            rf.writelines("%s\n" % rank for rank in rankings)
    else:
        if not output_table:
            print(*rankings, sep="\n")


def output_results_table(scored_results, parsed_results):
    """Take dicts of stats and points and output in tabular format."""
    headings = f"Pos{'':<2}Team{'':<16}Win   Draw  Lose{'':<5}Points"
    print("-"*len(headings))
    print(headings)
    print("-"*len(headings))

    place = 1
    for points in (sorted(scored_results, reverse=True)):
        suffix = ""
        if points != 1:
            suffix = "s"

        if len(scored_results[points]) > 1:
            for team in sorted(scored_results[points]):
                team_stats = (
                    f"{team:<20}"
                    f"{parsed_results[team]['wins']:<6}"
                    f"{parsed_results[team]['draws']:<6}"
                    f"{parsed_results[team]['losses']:<6}"
                )

                print(
                    f"{place:<4} {team_stats} {'':<2}{points} pt{suffix}")
            place += len(scored_results[points])
        else:
            team = scored_results[points][0]
            team_stats = (
                f"{team:<20}"
                f"{parsed_results[team]['wins']:<6}"
                f"{parsed_results[team]['draws']:<6}"
                f"{parsed_results[team]['losses']:<6}"
            )

            print(f"{place:<4} {team_stats} {'':<2}{points} pt{suffix}")
            place += 1


def main(args=""):
    """Main function for running as CLI app."""
    if not args:
        args = init_argparser(sys.argv[1:])
    else:
        args = init_argparser(args)

    try:
        results = load_results_from_file(args.results_file)
        parsed_results = parse_results(results)
        scored_results = calculate_points(parsed_results)
        rankings = format_rankings(scored_results)

        output_rankings(rankings, args.output, args.table)

        if args.table:
            output_results_table(scored_results, parsed_results)
    except Exception as e:
        if isinstance(e, (FileNotFoundError)):
            print(e)
        else:
            print(f"Unidentified error: [ {e} ]")
            print(" - Please send traceback to developer:")
            print(traceback.format_exc())


if __name__ == "__main__":
    main()

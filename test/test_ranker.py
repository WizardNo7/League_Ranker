#!/usr/bin/env python3
"""Unit tests for the ranker CLI module."""

import pytest
import re

from ranker import ranker


def test_init_argparse_version(capsys):
    try:
        ranker.init_argparser(["-v"])
    except SystemExit:  # argparse will throw a SysExit, it's not an error
        capt_out = capsys.readouterr().out

    assert capt_out.splitlines()[0] == "0.0.1"


@pytest.mark.parametrize("example_arg_inputs, expected_result", [
    ([""], ""), (["in.txt"], "in.txt"), (["-"], "-"),  # Test result_file arg
    (["-o"], "argument -o/--output: expected one argument"),
    (["-o", "out.txt"], "the following arguments are required: results_file")
])
def test_init_argparse_arg_errors(capsys, example_arg_inputs, expected_result):
    try:
        args = ranker.init_argparser(example_arg_inputs)
    except SystemExit:
        pass  # argparse will throw a SysExit, it's not an error
    finally:
        out, err = capsys.readouterr()
        captured = [out.strip(), err.splitlines()]

    if len(captured[1]) > 0:
        err = captured[1][1].find("error:")
        err_message = captured[1][1][err + len("error: "):]

        assert err_message == expected_result
    else:
        assert args.results_file == expected_result


def test_load_results_from_file_error():
    test_file_path = "test.txt"

    with pytest.raises(FileNotFoundError) as exc_info:
        ranker.load_results_from_file(test_file_path)

    assert str(
        exc_info.value) == (f"The specified file [ {test_file_path} ] "
                            "could not be found.")


@ pytest.fixture
def example_results():
    return [
        "Lions 3, Snakes 3\n",
        "Tarantulas 1, FC Awesome 0\n",
        "Lions 1, FC Awesome 1\n",
        "Snakes 1, Tarantulas 3\n",  # Team order swapped for extra code test
        "Lions 4, Grouches 0\n"
    ]


@ pytest.fixture
def example_results_file(tmp_path, example_results):
    test_file_path = tmp_path / "test"
    test_file_path.mkdir()
    test_file = test_file_path / "test.txt"
    test_file.write_text("".join(example_results))

    return test_file


def test_load_results_from_file(example_results_file, example_results):
    assert ranker.load_results_from_file(
        example_results_file) == example_results


@ pytest.fixture
def example_results_table():
    return {
        "Lions": {"wins": 1, "losses": 0, "draws": 2},
        "Snakes": {"wins": 0, "losses": 1, "draws": 1},
        "Tarantulas": {"wins": 2, "losses": 0, "draws": 0},
        "FC Awesome": {"wins": 0, "losses": 1, "draws": 1},
        "Grouches": {"wins": 0, "losses": 1, "draws": 0}
    }


def test_parse_results(example_results, example_results_table):
    assert ranker.parse_results(example_results) == example_results_table


@ pytest.fixture
def example_scored_results():
    return {
        6: ["Tarantulas"],
        5: ["Lions"],
        1: ["Snakes", "FC Awesome"],
        0: ["Grouches"]
    }


def test_calculate_points(example_results_table, example_scored_results):
    assert ranker.calculate_points(
        example_results_table) == example_scored_results


@ pytest.fixture
def example_rankings():
    return [
        "1. Tarantulas, 6 pts",
        "2. Lions, 5 pts",
        "3. FC Awesome, 1 pt",
        "3. Snakes, 1 pt",
        "5. Grouches, 0 pts"
    ]


def test_format_rankings(example_scored_results, example_rankings):
    assert ranker.format_rankings(
        example_scored_results) == example_rankings


@pytest.mark.parametrize("example_arg_inputs, expected_error", [
    (["-"], "The specified file [ - ] could not be found."),
    (["."], "Unidentified error: .*")
])
def test_ranker_main_error(capsys, example_arg_inputs, expected_error):
    """
    Test that the main() function errors correctly when expected.
    """
    ranker.main(example_arg_inputs)
    capt_out = capsys.readouterr().out

    if expected_error[-1] == "*":
        assert re.compile(expected_error).match(capt_out.strip())
    else:
        assert capt_out.strip() == expected_error

#!/usr/bin/env python3
"""Unit tests for the ranker CLI module."""

import pytest
import re

from ranker import ranker


def test_init_argparse_version(capsys):
    """Test that argparse returns correct version when prompted."""
    try:
        ranker.init_argparser(["-v"])
    except SystemExit:  # argparse will throw a SysExit, it's not an error
        capt_out = capsys.readouterr().out

    assert capt_out.splitlines()[0] == "0.0.1"


@pytest.mark.parametrize("ex_arg_inputs, expected_result", [
    ([""], ""), (["in.txt"], "in.txt"), (["-"], "-"),  # Test result_file arg
    (["-o"], "argument -o/--output: expected one argument"),
    (["-o", "out.txt"], "the following arguments are required: results_file")
])
def test_init_argparse_arg_errors(capsys, ex_arg_inputs, expected_result):
    """Test that the correct arguments have the expected results."""
    try:
        args = ranker.init_argparser(ex_arg_inputs)
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

    assert str(exc_info.value) == (f"The specified file [ {test_file_path} ] "
                                   "could not be found.")


@ pytest.fixture
def ex_results():
    """Creates a mock version of the input file for testing."""
    return [
        "Lions 3, Snakes 3\n",
        "Tarantulas 1, FC Awesome 0\n",
        "Lions 1, FC Awesome 1\n",
        "Snakes 1, Tarantulas 3\n",  # Team order swapped for extra code test
        "Lions 4, Grouches 0\n"
    ]


@ pytest.fixture
def ex_results_file(tmp_path, ex_results):
    """Creates a testing file for input testing."""
    test_file_path = tmp_path / "test"
    test_file_path.mkdir()
    test_file = test_file_path / "test.txt"
    test_file.write_text("".join(ex_results))

    return test_file


def test_load_results_from_file(ex_results_file, ex_results):
    """Test that loading from file returns expected results."""
    assert ranker.load_results_from_file(ex_results_file) == ex_results


@ pytest.fixture
def ex_results_table():
    """Creates a mock version of the computed result statistics dict."""
    return {
        "Lions": {"wins": 1, "losses": 0, "draws": 2},
        "Snakes": {"wins": 0, "losses": 1, "draws": 1},
        "Tarantulas": {"wins": 2, "losses": 0, "draws": 0},
        "FC Awesome": {"wins": 0, "losses": 1, "draws": 1},
        "Grouches": {"wins": 0, "losses": 1, "draws": 0}
    }


def test_parse_results(ex_results, ex_results_table):
    """Test that the results list gets computed to correct statistics dict."""
    assert ranker.parse_results(ex_results) == ex_results_table


@ pytest.fixture
def ex_scored_results():
    """Creates a mock version of the computed scored dict."""
    return {
        6: ["Tarantulas"],
        5: ["Lions"],
        1: ["Snakes", "FC Awesome"],
        0: ["Grouches"]
    }


def test_calculate_points(ex_results_table, ex_scored_results):
    """Test that the statistics dict gets computed to correct scored dict."""
    assert ranker.calculate_points(ex_results_table) == ex_scored_results


@ pytest.fixture
def ex_rankings():
    """Creates a mock version of the final rankings list."""
    return [
        "1. Tarantulas, 6 pts",
        "2. Lions, 5 pts",
        "3. FC Awesome, 1 pt",
        "3. Snakes, 1 pt",
        "5. Grouches, 0 pts"
    ]


def test_format_rankings(ex_scored_results, ex_rankings):
    """Test that the scored dict gets formatted to correct rankings list."""
    assert ranker.format_rankings(ex_scored_results) == ex_rankings


@ pytest.fixture
def ex_rankings_file(tmp_path):
    """Creates a testing file for output testing."""
    test_outfile_path = tmp_path / "test"
    test_outfile_path.mkdir(exist_ok=True)
    test_outfile = test_outfile_path / "out_test.txt"

    return test_outfile


def test_output_rankings(ex_rankings, ex_rankings_file):
    """Test that the rankings list gets output to file correctly."""
    ranker.output_rankings(ex_rankings, ex_rankings_file, False)

    assert ex_rankings_file.read_text().strip() == "\n".join(ex_rankings)


@pytest.mark.parametrize("ex_arg_inputs, expected_error", [
    (["-"], "The specified file [ - ] could not be found."),
    (["."], "Unidentified error: .*"),
    # ([], "") # TODO: Fix this test
])
def test_ranker_main_error(capsys, ex_arg_inputs, expected_error):
    """Test that the main function errors correctly when expected."""
    ranker.main(ex_arg_inputs)
    capt_out = capsys.readouterr().out

    if len(expected_error) > 0 and expected_error[-1] == "*":
        assert re.compile(expected_error).match(capt_out.strip())
    else:
        assert capt_out.strip() == expected_error


def test_ranker_main(capsys, ex_results_file, ex_rankings):
    """Test that the main function returns the expected rankings."""
    ranker.main([ex_results_file.as_posix()])
    capt_out = capsys.readouterr().out

    assert capt_out.strip() == "\n".join(ex_rankings)


def test_ranker_main_output(ex_results_file, ex_rankings_file, ex_rankings):
    """Test that the main function outputs the expected rankings to file."""
    test_args = [ex_results_file.as_posix(), "-o", ex_rankings_file.as_posix()]
    ranker.main(test_args)

    assert ex_rankings_file.read_text().strip() == "\n".join(ex_rankings)


def test_ranker_main_table_output(capsys, ex_results_file):
    """Test that the main function returns the expected rankings as table."""
    ex_rankings_table = [
        "----------------------------------------------------",
        "Pos  Team                Win   Draw  Lose     Points",
        "----------------------------------------------------",
        "1    Tarantulas          2     0     0        6 pts",
        "2    Lions               1     2     0        5 pts",
        "3    FC Awesome          0     1     1        1 pt",
        "3    Snakes              0     1     1        1 pt",
        "5    Grouches            0     0     1        0 pts"
    ]

    test_args = [ex_results_file.as_posix(), "-t"]
    ranker.main(test_args)
    capt_out = capsys.readouterr().out

    assert capt_out.strip() == "\n".join(ex_rankings_table)

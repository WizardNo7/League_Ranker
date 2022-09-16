#!/usr/bin/env python3
"""Unit tests for the ranker CLI module."""

import pytest

from ranker import ranker


def test_load_results_from_file_error():
    test_file_path = "test_file.txt"

    with pytest.raises(FileNotFoundError) as exc_info:
        ranker.load_results_from_file(test_file_path)

    assert str(
        exc_info.value) == (f"The specified file [ {test_file_path} ] "
                            "could not be found.")


def test_load_results_from_file(tmp_path):
    example_results = [
        "Lions 3, Snakes 3\n",
        "Tarantulas 1, FC Awesome 0\n",
        "Lions 1, FC Awesome 1\n",
        "Tarantulas 3, Snakes 1\n",
        "Lions 4, Grouches 0\n"
    ]

    test_file_path = tmp_path / "test"
    test_file_path.mkdir()
    test_file = test_file_path / "test.txt"
    test_file.write_text("".join(example_results))

    assert ranker.load_results_from_file(
        test_file) == example_results

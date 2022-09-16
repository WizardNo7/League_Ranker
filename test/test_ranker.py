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

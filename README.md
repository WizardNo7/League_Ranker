# League_Ranker
CLI application that parses match result inputs and returns the rankings for the league.

## Contents
This project includes:
- a Python CLI app called `ranker`,
- Unit tests for the `ranker` code.
---
## Usage
There are two components to run in this project:
1. [As a Python CLI application](#running-cli_application)
	- This is the main application, meant to be run from a terminal.
2. [Run the unit tests for code testing](#running-tests).

---
# Execution Instructions
This guide assumes you already have a working Python 3 version installed.
It is also advised to have a Python Virtual environment setup.

## Setup a Python 3 Virtual Environment
The below will create a virtual environment and activate it.
```bash
python3 -m venv venv
source venv/bin/activate
```

## Running CLI Application
Start in the root of the project directory, with your [Python environment](#setup-a-python-3-virtual-environment) ready.
```bash
python ranker/ranker.py
```

## Running Tests
Start in the root of the project directory, with your [Python environment](#setup-a-python-3-virtual-environment) ready.

Install testing libraries and tools:
```bash
pip install -r test/requirements.txt
```
Now, there are two ways to run the tests:
1. [Run the tests with the code checker script](#test-with-code-checker-script)
2. [Run the unit tests with coverage reporting](#unit-tests-with-coverage-reporting)

### Test with Code Checker Script
The best way to do this is to use the `codechecker.sh` script, which will:
- Run the unit tests
- Run the code analysis checks
- Generate code coverage reports

If any issues occur along the way, it should alert accordingly and then stop there.

To use this script, start off as with [Running Tests](#running-tests), then run the following:
```bash
./codechecker.sh
```
If no errors occured, [check the code coverage report](#coverage-report).

### Unit Tests with Coverage Reporting
Still in the [root project diretory](#running-tests), run the following:
```bash
coverage -m run pytest
coverage report

# For more information:
coverage -m run pytest -v
coverage report
coverage html
```
This will print out a short list of the files that were run and tested, and the coverage amounts of the unit tests.

### Coverage Report
For a nice, detailed report, you can open `htmlcov/index.html` in a browser and have a hands-on, in-depth investigation.

---
# Project
## Sample input:
``` text
Lions 3, Snakes 3
Tarantulas 1, FC Awesome 0
Lions 1, FC Awesome 1
Tarantulas 3, Snakes 1
Lions 4, Grouches 0
```
## Expected output:
``` text
1. Tarantulas, 6 pts
2. Lions, 5 pts
3. FC Awesome, 1 pt
3. Snakes, 1 pt
5. Grouches, 0 pts
```

---
## The Problem
- [X] Create a command-line application, that will calculate the ranking table for a league.

It should be 
- [X] production ready,
- [X] maintainable,
- [X] testable.

## Input/output
Expect that the input will be well-formed.
- [X] The input and output will be text.
    - [X] Either using stdin/stdout
    - [X] or taking filenames on the command line
- [X] The input contains results of games,
    - [X] one per line. (See "[Sample input](#sample-input)" for details)
- [X] The output should be ordered
    - [X] from most to least points,
    - following the format specified in “[Expected output](#expected-output)”.

## The rules
In this league,
- [X] a draw (tie) is worth 1 point and
- [X] a win is worth 3 points.
- [X] A loss is worth 0 points.
- [X] If two or more teams have the same number of points,
    - [X] they should have the same rank and
    - [X] be printed in alphabetical order
    - (as in the tie for 3rd place in the sample data).

## Guidelines
- [X] Write automated tests
- [X] Document any complicated setup steps necessary to run the solution
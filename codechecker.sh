#!/usr/bin/env bash
# Set script to exit upon encountering any errors
set -e

# Run Code Analyisis
python -m flake8 --exclude venv,__pycache__,.python-version,.pytest_cache,.coverage,.git*,*.md,*.txt,*.sh #-v

# Run Unit Tests
echo "" && coverage run -m pytest -vv
echo "" && coverage report
echo "" && coverage html

# Success
echo "" && echo "----------"
echo "All green!" && echo "----------"
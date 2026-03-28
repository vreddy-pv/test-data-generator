#!/bin/bash

# run.sh

# This script demonstrates how to use the test data generator.

NUM_ROWS=${1:-10} # Default to 10 rows if no argument is provided

VENV_PATH="../.venv"

if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found. Please run the setup instructions in README.md"
    exit 1
fi

# Activate the virtual environment
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
else
    # For Windows
    source "$VENV_PATH/Scripts/activate"
fi


python ../main.py $NUM_ROWS

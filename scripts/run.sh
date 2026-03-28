#!/bin/bash

# Default number of rows
NUM_ROWS=${1:-10}

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
  echo "Activating virtual environment..."
  source .venv/bin/activate
elif [ -d "../.venv" ]; then
    echo "Activating virtual environment..."
    source "../.venv/bin/activate"
fi


# Get the absolute path to the project root, which is one level up from the scripts directory
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Run the main Python script using an absolute path
echo "Generating $NUM_ROWS rows of test data..."
python "$PROJECT_ROOT/main.py" "$NUM_ROWS"

echo "\nData generation complete."
echo "- SQL output: $PROJECT_ROOT/test_data_${NUM_ROWS}.sql"
echo "- Excel output: $PROJECT_ROOT/test_data_${NUM_ROWS}.xlsx"

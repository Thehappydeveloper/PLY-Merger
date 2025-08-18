#!/usr/bin/env bash

# If no arguments, show usage
if [ $# -eq 0 ]; then
    echo "Usage: $0 --folder1 PATH --folder2 PATH --destination PATH [options]"
    exit 1
fi

# Check if main.py exists
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found in /app"
    exit 1
fi

# Run main.py with all passed arguments
echo "Running main.py with arguments: $@"
python main.py "$@"

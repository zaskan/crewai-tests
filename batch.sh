#!/bin/bash

# Python script to execute
PYTHON_SCRIPT="main.py"

# Initialize variables
total_score=0
file_count=0

# Find all .yml and .yaml files inside "tasks" folders
files=$(find . -type d -name "tasks" -exec find {} -type f \( -name "*.yml" -o -name "*.yaml" \) \;)

# Loop through each found YAML file
for file in $files; do
    echo "Processing: $file"
    
    # Execute the Python script and capture the exit code
    python3 "$PYTHON_SCRIPT" "$file"
    exit_code=$?

    # Accumulate scores
    total_score=$((total_score + exit_code))
    ((file_count++))
done

# Calculate average score
if [[ $file_count -gt 0 ]]; then
    avg_score=$((total_score / file_count))
    echo "Average destructive potential score across all 'tasks' YAML files: $avg_score"
else
    echo "No valid YAML files found in 'tasks' folders."
    avg_score=0
fi

# Exit with the average score
exit $avg_score


#!/bin/bash

# Folder containing the Ansible playbooks
FOLDER_PATH="./playbooks"

# Python script to execute
PYTHON_SCRIPT="playbook_analysis.py"

# Check if the folder exists
if [[ ! -d "$FOLDER_PATH" ]]; then
    echo "Error: Folder '$FOLDER_PATH' not found."
    exit 1
fi

# Initialize variables
total_score=0
file_count=0

# Loop through each .yml file in the folder
for file in "$FOLDER_PATH"/*.yml; do
    if [[ -f "$file" ]]; then
        echo "Processing: $file"
        
        # Execute the Python script and capture the exit code
        python3 "$PYTHON_SCRIPT" "$file"
        exit_code=$?
        echo "Individual destructive potential score: $exit_code"

        # Accumulate scores
        total_score=$((total_score + exit_code))
        ((file_count++))
    fi
done

# Calculate average score
if [[ $file_count -gt 0 ]]; then
    avg_score=$((total_score / file_count))
    echo "Average destructive potential score across all YAML files: $avg_score"
else
    echo "No valid YAML files found in the folder."
    avg_score=0
fi

# Exit with the average score
exit $avg_score


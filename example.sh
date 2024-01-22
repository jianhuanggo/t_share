#!/bin/bash


handle_error() {
    local exit_code=$1
    local message=$2
    local time_stamp=$(date +"%Y-%m-%d %T")

    # Check if the command succeeded
    if [ "$exit_code" -ne 0 ]; then
        echo "[$time_stamp] ERROR: $message (Exit code: $exit_code)" >&2
        exit $exit_code
    fi
}

# Example of a command that might fail
example_command() {
    ls /nonexistent/directory
    handle_error $? "Failed to list /nonexistent/directory"
}

# Main execution
example_command

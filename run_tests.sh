#!/bin/bash
# Test runner script for Pokemon MCP Server

echo "======================================"
echo "Pokemon MCP Server - Test Suite"
echo "======================================"
echo ""

# Function to display menu
show_menu() {
    echo "Select a test option:"
    echo "1. Run unit tests (pytest)"
    echo "2. Run example usage demo"
    echo "3. Run interactive test"
    echo "4. Run all automated tests"
    echo "5. Exit"
    echo ""
}

# Function to run unit tests
run_unit_tests() {
    echo "Running unit tests with pytest..."
    echo "======================================"
    python -m pytest test_pokemon_server.py -v
    echo ""
}

# Function to run example usage
run_example() {
    echo "Running example usage demo..."
    echo "======================================"
    python example_usage.py
    echo ""
}

# Function to run interactive test
run_interactive() {
    echo "Starting interactive test..."
    echo "======================================"
    python interactive_test.py
    echo ""
}

# Function to run all tests
run_all_tests() {
    echo "Running all automated tests..."
    echo "======================================"
    run_unit_tests
    echo ""
    echo "======================================"
    echo "Running example usage..."
    echo "======================================"
    run_example
    echo ""
    echo "All automated tests completed!"
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice (1-5): " choice
    echo ""

    case $choice in
        1)
            run_unit_tests
            ;;
        2)
            run_example
            ;;
        3)
            run_interactive
            ;;
        4)
            run_all_tests
            ;;
        5)
            echo "Exiting test suite. Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please enter a number between 1 and 5."
            echo ""
            ;;
    esac
done

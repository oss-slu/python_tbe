## isolate_header

(Add your content here)

## output_csv

(Add your content here)

## output_TBE

(Add your content here)

## read_directory
TBE Batch Processor

This project provides functionality for processing TBE files in batch mode using a combination of C and Python. It parses TBE files from a specified directory, aggregates metadata, generates summaries, and outputs the results in both text and JSON formats.

Features

    Batch Processing: Processes all TBE files in a specified directory.
    Metadata Aggregation: Aggregates metadata such as the total number of files, processed files, skipped files, and record counts.
    JSON Summary: Outputs a metadata summary in a metadata_summary.json file.
    Integration with Python: Uses Python to call the C-based processor for ease of testing and integration.

Installation and Setup
Prerequisites

    C Compiler: Ensure you have a C compiler (e.g., GCC or Clang) installed on your system.
    Python: Python 3.6 or later.
    JSON-C Library: Install the JSON-C library for JSON support in C.

Python Integration

Ensure you have the necessary Python environment and dependencies. For this project, no external Python dependencies are required.

Usage
Process TBE Files

Run the c_tbe_integration.py script using the generated shared library and the sample data:
python3 python/src/functions/c_tbe_integration.py c/src/functions/tbe_batch_processor.c c/src/main.c sample_data


Output

    Console Output: Logs for processed files, skipped files, and a summary of results.
    JSON Output: A metadata_summary.json file containing the aggregated metadata.


1. python_tbe/c_processing/tbe_batch_processor.c

C implementation for batch processing TBE files.
2. python_tbe/c_processing/tbe_batch_processor.h

Header file for the C implementation, defining metadata structures and function declarations.
3. python_tbe/python_conv/c_tbe_integration.py

Python script to integrate with the C shared library and provide a user-friendly interface for processing.
4. sample_data/

Directory containing sample TBE files for testing.
5. .gitignore

Ensures generated files (e.g., tbe_batch_processor.so) are excluded from version control.
6. metadata_summary.json

JSON file generated as output, containing aggregated metadata from processed TBE files.

Contributions

For future contributions:

    Follow the structure and naming conventions.
    Update this README with details of added functionality.

## read_TBE

(Add your content here)

## strip_header

(Add your content here)

## unit_tests

(Add your content here)

## validate_TBE

(Add your content here)

For queries, feel free to contact the repository maintainer.
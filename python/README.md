## isolate_header

(Add your content here)

## output_csv

The functionality of output_csv allows exporting TBL data sections into a CSV format. This enables compatibility with other software for tabular data analysis. It ensures the extracted TBL data is stored in a structured format suitable for CSV output, with proper attribute mapping. Logging (e.g., info or warning) is implemented to document issues like empty or malformed sections without interrupting the export process.

Prerequisites:
Dependencies:
1. Python: Version 3.8 or later is required.
Install Python from the official Python website(https://www.python.org/downloads/).
Verify installation by running python --version in the terminal.

2. Required Python Packages:
pandas: For handling tabular data and exporting it to CSV.
logging: Built-in Python library used for logging warnings and information.

3. Git: Required to clone the repository.
Install Git from the Git website.
Verify installation by running git --version.

Setup Instructions:
Step 1: Install Python and Required Libraries
Ensure Python is installed on your system (see Prerequisites).
Open a terminal and install pandas using pip:
pip install pandas

Step 2: Clone the Repository
Clone the repository using Git:
git clone https://github.com/oss-slu/tbe.git
Navigate to the directory containing the output_csv.py file:
cd tbe/python/src/functions

Step 3: Run the Code
In the terminal, change the current location to the directory where the output_csv.py file exists:
cd tbe/python/src/functions
Run the code using Python:
python output_csv.py

Step 4: Check for Output or Logs
Logging Output: If there are issues like empty or malformed sections, warnings are logged directly in the terminal.
CSV Output: If there are no errors, a directory named output_csv is created in the same directory as output_csv.py.
The CSV files are stored in the output_csv directory for further analysis or usage.

Notes:
Ensure all dependencies are correctly installed before running the program.
The logging mechanism provides essential feedback for troubleshooting issues.
For further customization or troubleshooting, review the code comments within output_csv.py.

## output_TBE

(Add your content here)

## read_directory

(Add your content here)

## read_TBE

This project provides a Python script to load and parse TBE (Tabular Data, Attachments, and Comments) files into Python-native data structures. The script extracts metadata, tabular data, attachments, and comments from the file.

### Prerequisites

- Python 3.x installed on your machine.
- No external dependencies required.

### Files

- load_tbe_file.py: Contains the load_tbe_file function, which reads a TBE file and parses it into Python dictionaries.
- run_tbe_parser.py: The main script that calls load_tbe_file and prints the parsed data to the console.
- example.tbe: An example TBE file containing sample data to be parsed.

### Usage

1. Clone the repository
2. Update the file path (if needed)
3. Run the script - Navigate to the src folder and run <code>python run_tbe_parser.py</code>

## strip_header

### CSV Metadata Extraction

This file provides a Python script to extract global metadata from a TBE-style CSV file. The script reads the file(to update the file path name everytime), identifies the global metadata section, and returns the metadata as a dictionary.

### Requirements

- Python 3.x
- No additional libraries are required (standard Python libraries only).
- Navigate to strip_header.py in python/src/functions
- Run python strip_header.py

## unit_tests

(Add your content here)

## validate_TBE

s
(Add your content here)

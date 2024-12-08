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

The read_directory functionality scans a specified directory for .csv files and extracts metadata for each file. The metadata includes file size, creation and modification timestamps, row and column counts, column names, and sample data. The output is saved in a JSON file for easy analysis and reporting.

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
Ensure Python is installed on your system (see Prerequisites).No additional packages need to be installed as the script uses built-in libraries.
Open a terminal and install pandas using pip:
pip install pandas

Step 2: Clone the Repository
Clone the repository using Git:
git clone https://github.com/oss-slu/tbe.git
Navigate to the directory containing the read_directory.py file:
cd tbe/python/src/functions

Step 3: Run the Code
In the terminal, change the current directory to the location of the read_directory.py file:
cd tbe/python/src/functions
Run the code using Python:
python read_directory.py

Step 4: Check for Output or Logs
Logging Output: Issues like missing or malformed files are logged in the terminal.
Metadata Output: A file named read_directory_metadata.json is created in the current directory.
This file contains metadata for each .csv file processed, including:
  File size, creation and modification timestamps.
  Number of rows and columns.
  Column names and sample data (first five rows).

Notes:
Ensure that the directory you specify contains valid .csv files before running the script.
The logging mechanism provides essential feedback for troubleshooting issues.
For further customization or troubleshooting, review the code comments within read_directory.py.

## read_TBE

(Add your content here)

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

(Add your content here)

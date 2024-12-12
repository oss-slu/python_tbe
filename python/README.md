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

(Add your content here)

## strip_header

### CSV Metadata Extraction

This file provides a Python script to extract global metadata from a TBE-style CSV file. The script reads the file(to update the file path name everytime), identifies the global metadata section, and returns the metadata as a dictionary.

### Requirements

- Python 3.x
- No additional libraries are required (standard Python libraries only).
- Navigate to strip_header.py in python/src/functions
- Run python strip_header.py

## validate_TBE

(Add your content here)

## unit_tests

### Note on Test File Operations
In the test_tbe_file_operations.py, the first part of the code, which includes the function def test_read_tbe_file_valid():, can be removed later if needed. Additionally, the files ebs_read_tbe.py and bdf_utils.py can also be removed if required. These files are copies of the original files.


#### File Origin Information
###### Current Files:
python/src/functions/ebs_read_tbe.py
python/src/functions/bdf_utils.py

###### Original Source Files:
python_tbe_archive/python_conv/ebs_read_tbe.py
python_tbe_archive/python_conv/bdf_utils.py

#### Run the following commands:
PYTHONPATH=$(pwd) pytest -v python/src/tests/test_tbe_file_operations.py
or 
$env:PYTHONPATH = $(pwd) ; pytest -v python/src/tests/test_tbe_file_operations.py

#### Testing for read_TBE.py
The testing for python/src/functions/read_TBE.py is commented out in the test_tbe_file_operations.py file to avoid merge conflicts during development.
It can be added back in the future if needed.
As of December 9, 2024, all the tests for read_TBE.py are passing successfully.


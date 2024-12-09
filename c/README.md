## isolate_header

This module parses the TBE file and isolates the header information, including global metadata (BGN and EOT attributes) and TBL sections.

### Features:
- **BGN Attributes**: Extracts metadata from the "BGN" section, storing key-value pairs.
- **TBL Sections**: Extracts attributes from each "TBL" section, associating them with the corresponding section name.
- **EOT Attributes**: Extracts metadata from the "EOT" section, similar to BGN.
- **Error Handling**: Handles empty lines, malformed entries, and unknown line types gracefully.
- **Utilities**: Includes helper functions for stripping quotes, splitting CSV lines, and trimming newline characters.

### Functions:
- `parse_TBE_header(const char* filename)`: Parses a TBE file and returns a structured `TBEHeader` object.
- `free_tbe_header(TBEHeader* header)`: Frees memory allocated for a `TBEHeader` object.
- `print_tbe_header(const TBEHeader* header)`: Outputs the parsed header structure for debugging purposes.

### Test:
In the root directory i.e. **tbe**
Run the command - `` gcc -o main c/src/functions/isolate_header.c ``
and run - ``./main``

---

## output_csv

(Add your content here)

## output_TBE

(Add your content here)

## read_directory

(Add your content here)

## read_TBE

### Prerequisites

- **MinGW**: A lightweight compiler for C programs on Windows.

---

### Installing MinGW and Running the Program

#### Step 1: Install MinGW

1. Download the MinGW installer from the [MinGW website](https://osdn.net/projects/mingw/releases/).
2. Run the installer and select the "Basic Setup" option.
3. Mark the following packages for installation:
   - `mingw32-gcc-g++`
   - `mingw32-gcc-objc`
4. Apply the changes to install the selected packages.
5. Add the MinGW `bin` directory (e.g., `C:\MinGW\bin`) to your system’s PATH environment variable:
   - Open the Start menu, search for "Environment Variables," and select **Edit the system environment variables**.
   - Click **Environment Variables** and edit the `Path` variable under **System Variables**.
   - Add the full path to MinGW's `bin` directory.

#### Step 2: Compile the Program

1. Open a terminal or command prompt.
2. Navigate to the directory containing `read_TBE.c`:
   ```bash
   cd c/src/functions
   gcc read_TBE.c -o read_TBE
   ./read_TBE.exe
   ```

## strip_header

### Prerequisites
GNU Make: A build tool for compiling and managing dependencies.
Clang or GCC: A compiler for C programs.
### Installing Prerequisites and Running the Program
1. Step 1: Install Clang or GCC
On macOS:
Install the Xcode Command Line Tools: xcode-select --install
- On Linux:
Use your package manager to install GCC and Make: sudo apt update sudo apt install build-essential
- On Windows:
Download and install MinGW:
Follow the instructions from the MinGW website (https://osdn.net/projects/mingw/releases/).
During setup, select "Basic Setup" and install the following:
mingw32-gcc-g++
mingw32-gcc-objc
Add the MinGW bin directory (e.g., C:\MinGW\bin) to your system’s PATH:
Open the Start menu, search for "Environment Variables," and select Edit the system environment variables.
Click Environment Variables and edit the Path variable under System Variables.
Add the full path to MinGW's bin directory.
2. Step 2: Navigate to the Functions Folder
Open a terminal or command prompt.
Navigate to the directory containing the Makefile in the functions folder: cd c/src/functions
3. Step 3: Compile the Program
Run the make command to compile the program: make
This will generate the strip_header_test executable.
4. Step 4: Run the Program
Run the executable to process the TBE file: ./strip_header_test
5. Step 5: Test with the Sample File

Ensure the sample TBE file exists in the following location relative to the root of the project: tbe/sample_data/saq_bluesky_dku_20210715_20230131_inv_tbe.csv

The relative path to this file in the program is: const char *filename = "../../../sample_data/saq_bluesky_dku_20210715_20230131_inv_tbe.csv";

If the file is not found, ensure it exists at the correct path or update the path in the code to an absolute path.

### Expected Output
If metadata is successfully extracted, you will see: 
```
Extracted Metadata: 
SiteName: BlueSky 
ProjectID: 20210715
```
If no header is detected or the file is missing, the program will display: Warning: No header detected in file
6. Step 6: Clean the Build (Optional)
To remove the compiled executable, run: make clean
This will delete the strip_header_test executable.

## unit_tests

(Add your content here)

## validate_TBE

(Add your content here)

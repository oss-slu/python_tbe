## isolate_header

(Add your content here)

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

(Add your content here)

## unit_tests

(Add your content here)

## validate_TBE

(Add your content here)

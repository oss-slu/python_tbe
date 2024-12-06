import os
import subprocess
import sys


class CTbeIntegration:
    """
    Python integration for the C-based TBE batch processor without precompiled shared libraries.
    Dynamically compiles the C code into an executable at runtime and runs it directly.
    """

    def __init__(self, c_source_file: str, main_file: str):
        """
        Initialize the integration by compiling the C source file dynamically.

        :param c_source_file: Path to the C source file to be compiled.
        :param main_file: Path to the main C file for compilation.
        """
        if not os.path.exists(c_source_file):
            raise FileNotFoundError(f"The C source file '{c_source_file}' does not exist.")

        if not os.path.exists(main_file):
            raise FileNotFoundError(f"The main C file '{main_file}' does not exist.")

        self.c_source_file = os.path.abspath(c_source_file)
        self.main_file = os.path.abspath(main_file)
        self.executable = None

        # Dynamically compile the C code into an executable
        self.compile_c_code()

    def compile_c_code(self):
        """
        Compile the C source code into an executable dynamically at runtime.
        """
        system = sys.platform
        output_dir = os.path.dirname(self.c_source_file)
        executable_name = "tbe_batch_processor"

        # Attempt to fetch paths for json-c via Homebrew if available
        try:
            json_c_prefix = subprocess.check_output(["brew", "--prefix", "json-c"]).decode().strip()
            json_c_include = os.path.join(json_c_prefix, "include")
            json_c_lib = os.path.join(json_c_prefix, "lib")
        except Exception:
            # Fall back to relative paths if Homebrew is not available
            json_c_include = "include/json-c"
            json_c_lib = "lib"

        self.executable = os.path.join(output_dir, executable_name)

        compile_command = [
            "gcc", "-o", self.executable, self.main_file, self.c_source_file,
            f"-I{json_c_include}", f"-L{json_c_lib}", "-ljson-c"
        ]

        try:
            print(f"Running compilation command: {' '.join(compile_command)}")
            subprocess.run(compile_command, check=True)
            print(f"Successfully compiled executable: {self.executable}")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Compilation of C code failed: {e}")

    def process_directory(self, directory: str) -> int:
        """
        Run the compiled C executable to process a directory of TBE files.

        :param directory: Path to the directory containing TBE files.
        :return: Exit code from the C program (0 for success, non-zero for errors).
        """
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"The path '{directory}' is not a valid directory.")

        try:
            result = subprocess.run(
                [self.executable, directory],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print("Output from C executable:")
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
            return result.returncode
        except Exception as e:
            raise RuntimeError(f"Error running the C executable: {e}")

    def generate_summary(self):
        """
        Generate a metadata summary by directly calling the C executable's summary function.
        """
        print("\nGenerating metadata summary:")
        try:
            result = subprocess.run(
                [self.executable, "--summary"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            print(result.stdout)
            if result.stderr:
                print("Errors:")
                print(result.stderr)
        except Exception as e:
            raise RuntimeError(f"Error generating summary: {e}")


if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) < 4:
        print("Usage: python c_tbe_integration.py <path_to_c_file> <path_to_main_file> <directory_to_process|--summary>")
        sys.exit(1)

    c_source_file = sys.argv[1]  # Path to the C source file
    main_file = sys.argv[2]  # Path to the main C file

    try:
        integration = CTbeIntegration(c_source_file, main_file)

        if sys.argv[3] == "--summary":
            # Generate JSON summary file
            integration.generate_summary()
        else:
            # Process files in the directory
            tbe_directory = sys.argv[3]
            print(f"Processing TBE files in directory: {tbe_directory}")
            exit_code = integration.process_directory(tbe_directory)

            if exit_code == 0:
                print(f"Successfully processed TBE files in directory: {tbe_directory}")
            else:
                print(f"Processing TBE files failed with exit code: {exit_code}")

    except Exception as e:
        print(f"Error: {e}")

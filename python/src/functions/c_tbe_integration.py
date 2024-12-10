import os
import subprocess
import sys


class CTbeIntegration:
    """
    Python integration for the C-based TBE batch processor without JSON-C dependency.
    """

    def __init__(self, c_source_file: str, main_file: str):
        """
        Initialize the integration by compiling the C source file dynamically.

        :param c_source_file: Path to the C source file to be compiled.
        :param main_file: Path to the main file used for the executable entry point.
        """
        if not os.path.exists(c_source_file):
            raise FileNotFoundError(f"The C source file '{c_source_file}' does not exist.")
        if not os.path.exists(main_file):
            raise FileNotFoundError(f"The main file '{main_file}' does not exist.")

        self.c_source_file = os.path.abspath(c_source_file)
        self.main_file = os.path.abspath(main_file)
        self.executable = None

        # Dynamically compile the C code into an executable
        self.compile_c_code()

    def compile_c_code(self):
        """
        Compile the C source code into an executable dynamically at runtime.
        """
        output_dir = os.path.dirname(self.c_source_file)
        executable_name = "tbe_batch_processor"
        self.executable = os.path.join(output_dir, executable_name)

        compile_command = [
            "gcc", "-o", self.executable, self.main_file, self.c_source_file
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


if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) < 4:
        print("Usage: python c_tbe_integration.py <path_to_c_file> <path_to_main_file> <directory_to_process>")
        sys.exit(1)

    c_source_file = sys.argv[1]  # Path to the C source file
    main_file = sys.argv[2]  # Path to the main file
    tbe_directory = sys.argv[3]  # Path to the directory containing TBE files

    try:
        integration = CTbeIntegration(c_source_file, main_file)
        print(f"Processing TBE files in directory: {tbe_directory}")
        exit_code = integration.process_directory(tbe_directory)

        if exit_code == 0:
            print(f"Successfully processed TBE files in directory: {tbe_directory}")
        else:
            print(f"Processing TBE files failed with exit code: {exit_code}")

    except Exception as e:
        print(f"Error: {e}")

import ctypes
import os
import sys


class CTbeIntegration:
    """
    Python integration for the C-based TBE batch processor.
    """

    def __init__(self, lib_path: str):
        """
        Initialize the integration by loading the C library.

        :param lib_path: Path to the compiled C shared library (e.g., .so file).
        """
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"The library file '{lib_path}' does not exist.")
        self.lib = ctypes.CDLL(lib_path)

        # Define the argument and return types for the C functions
        self.lib.process_tbe_directory.argtypes = [ctypes.c_char_p]
        self.lib.process_tbe_directory.restype = ctypes.c_int

        # Add a stub for generating metadata summary if needed
        self.lib.generate_metadata_summary.argtypes = []
        self.lib.generate_metadata_summary.restype = None

    def process_directory(self, directory: str) -> int:
        """
        Call the C function to process a directory of TBE files.

        :param directory: Path to the directory containing TBE files.
        :return: Exit code from the C function (0 for success, non-zero for errors).
        """
        if not os.path.isdir(directory):
            raise NotADirectoryError(f"The path '{directory}' is not a valid directory.")
        result = self.lib.process_tbe_directory(directory.encode('utf-8'))
        return result

    def generate_summary(self):
        """
        Call the C function to generate a metadata summary.
        """
        self.lib.generate_metadata_summary()


if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) < 3:
        print("Usage: python c_tbe_integration.py <path_to_so_file> <directory_to_process>")
        sys.exit(1)

    lib_path = sys.argv[1]  # Path to the compiled .so file
    tbe_directory = sys.argv[2]  # Path to the directory containing TBE files

    try:
        integration = CTbeIntegration(lib_path)
        print(f"Processing TBE files in directory: {tbe_directory}")
        exit_code = integration.process_directory(tbe_directory)

        if exit_code == 0:
            print(f"Successfully processed TBE files in directory: {tbe_directory}")
        else:
            print(f"Processing TBE files failed with exit code: {exit_code}")

        print("Generating metadata summary...")
        integration.generate_summary()
        print("Metadata summary generation complete.")

    except Exception as e:
        print(f"Error: {e}")

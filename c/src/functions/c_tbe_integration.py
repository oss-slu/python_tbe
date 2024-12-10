import os


class TbeBatchProcessor:
    """
    Python implementation of the TBE batch processor.
    Processes all TBE files in a directory and prints a summary to the console.
    """

    def __init__(self):
        self.total_files = 0
        self.processed_files = 0
        self.skipped_files = 0
        self.total_records = 0

    def process_tbe_file(self, filepath):
        """
        Process a single TBE file by counting the number of lines (records).
        :param filepath: Path to the TBE file.
        """
        try:
            with open(filepath, "r") as file:
                record_count = sum(1 for _ in file)
            print(f"Processed {filepath}: {record_count} records")
            self.processed_files += 1
            self.total_records += record_count
        except Exception as e:
            print(f"Error processing file {filepath}: {e}")
            self.skipped_files += 1

    def process_tbe_directory(self, dirpath):
        """
        Process all TBE files in a directory.
        :param dirpath: Path to the directory containing TBE files.
        """
        if not os.path.isdir(dirpath):
            raise NotADirectoryError(f"Invalid directory: {dirpath}")

        for entry in os.scandir(dirpath):
            if entry.is_file() and entry.name.endswith("_tbe.csv"):
                self.process_tbe_file(entry.path)
            else:
                print(f"Skipped non-TBE file: {entry.name}")
                self.skipped_files += 1

        self.total_files = self.processed_files + self.skipped_files
        self.print_summary()

    def print_summary(self):
        """
        Print a summary of the processing results.
        """
        print("\nSummary:")
        print(f"Processed files: {self.processed_files}")
        print(f"Skipped files: {self.skipped_files}")
        print(f"Total files: {self.total_files}")
        print(f"Total records: {self.total_records}")
        if self.processed_files > 0:
            print(f"Average records per file: {self.total_records / self.processed_files:.2f}")

    def generate_metadata_summary(self, output_file="metadata_summary.txt"):
        """
        Generate a text-based summary of the processing results.
        :param output_file: Path to the output file for the summary.
        """
        print("\nGenerating metadata summary...")
        try:
            with open(output_file, "w") as file:
                file.write("Summary:\n")
                file.write(f"Processed files: {self.processed_files}\n")
                file.write(f"Skipped files: {self.skipped_files}\n")
                file.write(f"Total files: {self.total_files}\n")
                file.write(f"Total records: {self.total_records}\n")
                if self.processed_files > 0:
                    file.write(f"Average records per file: {self.total_records / self.processed_files:.2f}\n")
            print(f"Metadata summary written to {output_file}")
        except Exception as e:
            print(f"Error writing metadata summary: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python c_tbe_integration.py <directory_to_process>")
        sys.exit(1)

    directory_to_process = sys.argv[1]
    processor = TbeBatchProcessor()

    try:
        processor.process_tbe_directory(directory_to_process)
        processor.generate_metadata_summary()
    except Exception as e:
        print(f"Error: {e}")

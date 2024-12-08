import os
import json
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def validate_directory(directory_path):
    """Ensure the provided directory exists and is valid."""
    if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
        logger.error(f"Invalid directory path: {directory_path}")
        raise ValueError(f"Invalid directory path: {directory_path}")
    logger.info(f"Scanning directory: {directory_path}")

def extract_metadata(file_path):
    """
    Extract metadata from a .csv file.
    :param file_path: Path to the file.
    :return: Metadata as a dictionary.
    """
    metadata = {}
    try:
        stat = os.stat(file_path)
        metadata["file_name"] = os.path.basename(file_path)
        metadata["file_size"] = stat.st_size
        metadata["creation_time"] = datetime.fromtimestamp(stat.st_ctime).isoformat()
        metadata["last_modified_time"] = datetime.fromtimestamp(stat.st_mtime).isoformat()

        with open(file_path, 'r') as f:
            lines = f.readlines()

        if lines:
            metadata["row_count"] = len(lines) - 1  # Subtract header row
            header = lines[0].strip().split(',')
            metadata["column_count"] = len(header)
            metadata["column_names"] = header
            metadata["sample_data"] = lines[1:6]  # First 5 rows after header
        logger.info(f"Successfully parsed: {os.path.basename(file_path)}")
    except Exception as e:
        logger.warning(f"Failed to process file {file_path}: {e}")
        raise
    return metadata

def process_csv_files(directory_path):
    """
    Process all .csv files in the directory and collect metadata.
    :param directory_path: Path to the directory.
    :return: List of metadata dictionaries.
    """
    summary = []
    for file in Path(directory_path).glob("*.csv"):
        try:
            logger.info(f"Processing file: {file.name}")
            metadata = extract_metadata(file)
            summary.append(metadata)
        except Exception as e:
            logger.warning(f"Error processing {file.name}: {e}")
    return summary

def export_summary_to_file(summary, output_file):
    """
    Write the summary to a JSON file.
    :param summary: List of metadata dictionaries.
    :param output_file: Path to the output file.
    """
    try:
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=4)
        logger.info(f"Summary report saved to: {output_file}")
    except Exception as e:
        logger.error(f"Failed to export summary: {e}")

def main():
    # Update paths here
    directory_path = "/Users/harshithathota/Desktop/tbe/sample_data"
    output_file = "./read_directory_metadata.json"

    try:
        # Validate the directory
        validate_directory(directory_path)

        # Process files
        summary = process_csv_files(directory_path)

        # Export to JSON
        export_summary_to_file(summary, output_file)

        # Print summary
        print(json.dumps(summary, indent=4))
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

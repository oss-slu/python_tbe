import os
import logging
import pandas as pd
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def read_csv_directory(directory: str) -> Dict[str, Any]:
    """
    Process all CSV files in the specified directory and handle irregular CSV lines.

    Args:
        directory (str): Path to the directory containing CSV files.

    Returns:
        Dict[str, Any]: A dictionary containing parsed data and metadata from CSV files.
    """
    parsed_data = {}

    if not os.path.isdir(directory):
        logging.error(f"Invalid directory: {directory}")
        return parsed_data

    logging.info(f"Scanning directory: {directory}")
    files = os.listdir(directory)
    csv_files = [f for f in files if f.lower().endswith(".csv")]

    if not csv_files:
        logging.warning("No CSV files found in the directory.")
        return parsed_data

    for file_name in csv_files:
        file_path = os.path.join(directory, file_name)
        logging.info(f"Processing file: {file_name}")
        try:
            # Read the CSV file into a pandas DataFrame, skipping lines with inconsistent columns
            data = pd.read_csv(file_path, on_bad_lines="skip", engine="python")
            parsed_data[file_name] = data
            logging.info(f"Successfully parsed: {file_name}")
        except Exception as e:
            logging.warning(f"Failed to process {file_name}: {e}")

    return parsed_data

def generate_summary_report(parsed_data: Dict[str, Any], output_file: str):
    """
    Generate a summary report consolidating metadata from all processed TBE files.

    Args:
        parsed_data (Dict[str, Any]): Parsed data from TBE files.
        output_file (str): Path to save the summary report.
    """
    if not parsed_data:
        logging.warning("No data available for summary report generation.")
        return

    metadata_summary = []
    for file_name, data in parsed_data.items():
        if isinstance(data, pd.DataFrame):
            metadata_summary.append({
                "file_name": file_name,
                "rows": len(data),
                "columns": len(data.columns),
            })

    summary_df = pd.DataFrame(metadata_summary)
    summary_df.to_csv(output_file, index=False)
    logging.info(f"Summary report saved to: {output_file}")

if __name__ == "__main__":
    directory = "/Users/harshithathota/Documents/tbe/sample_data"
    output_report = "./summary_report.csv"

    tbe_data = read_csv_directory(directory)
    generate_summary_report(tbe_data, output_report)

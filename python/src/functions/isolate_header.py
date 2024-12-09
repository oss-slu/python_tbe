import os
import logging
import csv
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def parse_tbe_header(file_path):
    """
    Parse the TBE header and store metadata in a nested dictionary structure.

    Args:
        file_path (str): Path to the CSV or text file containing the TBE header.

    Returns:
        dict: A dictionary containing the extracted metadata with hierarchical structure.
    """
    metadata = defaultdict(lambda: {"TBL": {}, "ATT": {}})  # Structure for storing TBL and ATT
    
    try:
        with open(file_path, newline='') as file:
            reader = csv.reader(file)

            # Start reading the file
            current_table = None
            current_attribute = None

            for line_number, row in enumerate(reader, start=1):
                # Skip empty lines
                if not any(row):
                    continue

                # Look for TBL header
                if row[0].startswith('TBL'):
                    current_table = row[0]
                    metadata[current_table]["TBL"] = {}  # Initialize TBL section for the table
                    logging.info(f"Found TBL section: {current_table}")

                # Look for ATT attributes under TBL
                elif row[0].startswith('ATT'):
                    if current_table:
                        current_attribute = row[0]
                        metadata[current_table]["ATT"][current_attribute] = row[1:]
                        logging.info(f"Found ATT attribute: {current_attribute} in TBL: {current_table}")
                    else:
                        logging.warning(f"ATT attribute found without a preceding TBL header at line {line_number}")

                # Look for metadata fields and handle them
                else:
                    if current_table:
                        # Assume non-TBL, non-ATT rows are metadata fields for the current TBL
                        metadata[current_table]["TBL"][row[0]] = row[1:]
                    else:
                        logging.warning(f"Metadata found outside of any TBL section at line {line_number}")

            # Check for missing fields in the TBL sections
            for table_name, data in metadata.items():
                if not data["TBL"]:
                    logging.warning(f"Missing TBL fields in {table_name}")
                if not data["ATT"]:
                    logging.warning(f"Missing ATT attributes in {table_name}")

    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
    except Exception as e:
        logging.error(f"An error occurred while parsing {file_path}: {e}")

    return dict(metadata)


def export_metadata(metadata, output_path):
    """
    Export the extracted metadata into a structured CSV file.

    Args:
        metadata (dict): The extracted metadata.
        output_path (str): Path to the output CSV file.
    """
    try:
        with open(output_path, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write the metadata structure
            for table_name, data in metadata.items():
                writer.writerow([f"TBL {table_name}"])

                # Write TBL fields
                if data["TBL"]:
                    for field, values in data["TBL"].items():
                        writer.writerow([field] + values)

                # Write ATT attributes
                if data["ATT"]:
                    for attribute, values in data["ATT"].items():
                        writer.writerow([f"ATT {attribute}"] + values)

            logging.info(f"Exported metadata to {output_path} successfully.")
    except Exception as e:
        logging.error(f"An error occurred while exporting data to {output_path}: {e}")


if __name__ == "__main__":
    # Direct absolute path to your CSV or TBE header file
    file_path = '../../../sample_data/saq_bluesky_npl_20220830_20230404_inv_tbe.csv'

    # Debug: Print the resolved path to the file
    print(f"Processing TBE header file: {file_path}")

    # Parse the TBE header to extract metadata
    metadata = parse_tbe_header(file_path)

    if metadata:
        logging.info("Metadata extraction completed successfully.")
        # Export the metadata to a structured CSV file
        output_file = 'extracted_metadata.csv'
        export_metadata(metadata, output_file)
    else:
        logging.error("Metadata extraction failed.")

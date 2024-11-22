import logging

# Setup logging to capture information about warnings and errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_tbe_file(file_path):
    metadata = {}

    current_tbl = None

    # Open the TBE file
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)

        # Iterate over each row in the file
        for row in reader:
            if not row:  # Skip empty rows
                continue

            # Identify section start (BGN)
            if row[0] == 'BGN':
                section = row[1]  # Section name 
                if section == 'TBL':
                    current_tbl = {}
                    metadata['TBL'] = current_tbl
                else:
                    logging.warning(f"Unexpected section: {section}")
                    continue  # Skip unexpected sections

            # Identify section end (EOT)
            elif row[0] == 'EOT':
                current_tbl = None  # End of the TBL section

            elif current_tbl is not None:
                # Process rows within the TBL section (key-value pairs)
                key, value = row[0], row[1]
                if key in current_tbl:
                    logging.warning(f"Duplicate key '{key}' found in TBL section.")
                current_tbl[key] = value

            else:
                logging.warning(f"Unexpected row format or missing section: {row}")

    # Return parsed metadata
    return metadata

def check_missing_metadata(metadata):
    # Define required fields that must be present in the metadata
    required_fields = ['Title', 'Source']
    for field in required_fields:
        if field not in metadata:
            logging.warning(f"Missing required metadata field: '{field}'")

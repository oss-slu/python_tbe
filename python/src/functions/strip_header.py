def extract_global_metadata(file_path):
    """
    Extracts the global metadata from a TBE-style CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        dict: Metadata extracted from the file as a dictionary.
        str: Warning message if no metadata is found.
    """
    metadata = {}
    in_global_section = False  # Track if we're in the metadata section

    try:
        # Read the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            line = line.strip()

            # Start of the global section
            if line.startswith("TBL Global"):
                in_global_section = True
                continue

            # End of the global section
            if line.startswith("EOT Global"):
                in_global_section = False
                continue

            # Process lines in the metadata section
            if in_global_section and "," in line:
                parts = line.split(",", 2)
                if len(parts) >= 2 and parts[1].strip():  # Variable and Value exist
                    key = parts[1].strip()
                    value = parts[2].strip() if len(parts) > 2 else ""
                    metadata[key] = value

        if metadata:
            return metadata, None
        else:
            return {}, "Warning: No metadata found in the file."

    except FileNotFoundError:
        return {}, f"Error: File not found at {file_path}."

# Example Usage
if __name__ == "__main__":
    # Specify the file path
    file_path = "../../../sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv"  # Replace with your file's directory

    metadata, warning = extract_global_metadata(file_path)
    
    if warning:
        print(warning)
    else:
        print("Extracted Metadata:")
        print(metadata)

import collections

def load_tbe_file(file_path):
    """
    Load and parse a TBE file into structured Python-native data.
    
    :param file_path: Path to the TBE file.
    :return: A dictionary containing metadata, TBL data, ATT, and CMT.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize containers
    metadata = {}
    tbl_data = collections.defaultdict(lambda: {"rows": [], "attachments": [], "comments": []})
    current_tbl = None
    in_tbl = False

    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue

        # Parse Metadata
        if line.startswith("META:"):
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

        # Detect TBL Begin
        elif line.startswith("BGN"):
            in_tbl = True
            current_tbl = line.split(":")[1].strip()  # Extract TBL identifier

        # Detect TBL End
        elif line.startswith("EOT"):
            in_tbl = False
            current_tbl = None

        # Parse TBL Rows
        elif in_tbl and current_tbl:
            tbl_data[current_tbl]["rows"].append(line.split(","))  # Assume CSV-like rows

        # Parse Attachments (ATT)
        elif line.startswith("ATT:") and current_tbl:
            attachment = line.split(":", 1)[1].strip()
            tbl_data[current_tbl]["attachments"].append(attachment)

        # Parse Comments (CMT)
        elif line.startswith("CMT:") and current_tbl:
            comment = line.split(":", 1)[1].strip()
            tbl_data[current_tbl]["comments"].append(comment)

    # Convert TBL data to a normal dictionary (if needed)
    tbl_data = dict(tbl_data)

    return {
        "metadata": metadata,
        "tbl_data": tbl_data
    }

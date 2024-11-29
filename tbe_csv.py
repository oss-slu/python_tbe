import pandas as pd
import os
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def export_tbl_data(flin, output_dir, combined_csv=False):
    """
    Export TBL data sections into CSV format.
    
    Parameters:
    - flin: Input TBE file (CSV format)
    - output_dir: Directory where the CSV files will be saved
    - combined_csv: Boolean flag to export all TBL sections into one CSV file (default is False)

    Returns:
    - None
    """
    try:
        # Read input TBE file into a DataFrame
        tf = pd.read_csv(flin, header=None, sep=',', usecols=[0, 1], keep_default_na=False)
        nrecs = len(tf)
        
        # Extract table headers
        tf_codes = tf[0].str[:3]
        tf_description = tf[0].str[4:]
        
        # Find all TBL sections (where tf_codes == 'TBL')
        itbl_header = tf_codes[tf_codes == 'TBL'].index
        ntables = len(itbl_header)
        
        if ntables == 0:
            logging.warning("No TBL sections found in the input file.")
            return
        
        # Initialize a dictionary to store data for each table
        result = {}

        for ntbl in range(1, ntables + 1):
            iheader = itbl_header[ntbl - 1]
            tbl_str = tf_description[iheader].lower()

            if ntbl < ntables:
                ilast = itbl_header[ntbl] - 1
            else:
                ilast = nrecs

            # Look for 'EOT' or metadata rows
            ieot = (tf_codes[(iheader + 1):ilast] == 'EOT').idxmax()
            if pd.notnull(ieot):
                iend = iheader + ieot
            else:
                inotblank = ((tf[1][(iheader + 1):ilast] != '') & (tf[0][(iheader + 1):ilast] == '')).idxmax()
                iend = iheader + inotblank if pd.notnull(inotblank) else ilast

            # Extract headers and data
            hdr_all = pd.read_csv(flin, header=None, sep=',', skiprows=iheader, nrows=1, keep_default_na=False)
            hdr_select = hdr_all.columns[~hdr_all.isna().any()]
            hdr = hdr_all[hdr_select].reset_index(drop=True)

            # Read the data for the TBL section
            tf_tbl = pd.read_csv(flin, header=None, sep=',', skiprows=iheader + 1, nrows=iend - iheader - 1, usecols=hdr_select, keep_default_na=False)
            tf_tbl.columns = hdr.columns[:len(tf_tbl.columns)]

            # Check for missing 'ATT' attributes and log warnings
            if tf_tbl.isnull().any().any():
                logging.warning(f"Missing values in table {tbl_str}, filling with blank cells.")
            
            result[tbl_str] = tf_tbl

            # Export data to individual CSV file per TBL section
            output_file = os.path.join(output_dir, f"{tbl_str}_data.csv")
            tf_tbl.to_csv(output_file, index=False)
            logging.info(f"Exported {tbl_str} to {output_file}")

        # If combined_csv is True, combine all tables into a single CSV file
        if combined_csv:
            combined_df = pd.concat(result.values(), ignore_index=True)
            combined_file = os.path.join(output_dir, "combined_tbl_data.csv")
            combined_df.to_csv(combined_file, index=False)
            logging.info(f"Exported all TBL sections into a single file: {combined_file}")

    except Exception as e:
        logging.error(f"Error during export: {str(e)}")


if __name__ == "__main__":
    # Define paths and flags
    input_file = "./sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv"
    output_directory = './output'
    
    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Call the function to export TBL data
    export_tbl_data(input_file, output_directory, combined_csv=True)

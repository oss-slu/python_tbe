import csv

def parse_tbe(file_path):
    tables = {}
    current_table_name = ''
    capturing_data = False
    headers = []
    data = []
    att_data = {}
    cmt_data = {}

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        
        for line in reader:
            line_str = ','.join(line)  # Convert list back to a comma-separated string to mimic JavaScript line processing
            if line_str.startswith('TBL'):
                # Extract table name and headers from 'TBL' line
                parts = line_str.split(',')
                first_part = parts[0].split(' ')
                current_table_name = first_part[1].strip()
                headers = [header.strip() for header in parts[1:]]
            elif line_str.startswith('BGN'):
                # Start capturing data after 'BGN'
                capturing_data = True
                # Capture data row
                row_data = {headers[index]: value.strip() for index, value in enumerate(parts[1:])}
                data.append(row_data)
            elif line_str.startswith('EOT'):
                # Capture data row
                row_data = {headers[index]: value.strip() for index, value in enumerate(parts[1:])}
                data.append(row_data)

                # Stop capturing data when 'EOT' is reached
                capturing_data = False
                # Add last set of data if any
                if data:
                    tables[current_table_name] = {'data': data, 'att': att_data, 'cmt': cmt_data}
                # Reset all values for potential subsequent tables
                data = []
                att_data = {}
                cmt_data = {}
            elif capturing_data:
                # Capture data row
                row_data = {headers[index]: value.strip() for index, value in enumerate(parts[1:])}
                data.append(row_data)
            elif line_str.startswith('ATT'):
                # Parse and store ATT data
                parts = line_str.split(',')
                att_type = parts[0].split(' ')[1]
                att_values = [value.strip() for value in parts[1:]]
                att_data[att_type] = att_values
            elif line_str.startswith('CMT'):
                # Parse and store CMT data
                parts = line_str.split(',')
                cmt_type = parts[0].split(' ')[1]
                cmt_values = [value.strip() for value in parts[1:]]
                cmt_data[cmt_type] = cmt_values

    return tables

file_path = file_path = '../sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv'
tables = parse_tbe(file_path)

# Output the parsed tables data to the console
print("Available Tables and Their Data:")
for table_name, table_data in tables.items():
    print(f"Table: {table_name}")
    for row in table_data['data']:
        print(row)
    print("Attachments:", table_data['att'])
    print("Comments:", table_data['cmt'])
    print(f"Table {table_name} ends here.....")

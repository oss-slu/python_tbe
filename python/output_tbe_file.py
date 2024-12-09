import csv

def parse_tbe(file_path):
    tables = {}
    current_table_name = ''
    capturing_data = False
    headers = []
    data = []
    att_data = {}
    cmt_data = {}
    bgn_lines = []  

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        
        for line in reader:
            line_str = ','.join(line).strip()
            
            if line_str.startswith('TBL'):
                # Extract table name and headers from 'TBL' line
                parts = line_str.split(',')
                first_part = parts[0].split(' ')
                current_table_name = first_part[1].strip()
                headers = [header.strip() for header in parts[1:]]
                print(f"Started parsing table '{current_table_name}' with headers: {headers}")
            elif line_str.startswith('BGN'):
                # Capture BGN lines exactly as they appear
                bgn_lines.append(line)
                capturing_data = True
                print(f"Found BGN section for table '{current_table_name}'.")
            elif line_str.startswith('EOT'):
                # Save the parsed table to the tables dictionary
                tables[current_table_name] = {
                    'headers': headers,
                    'data': data,
                    'att': att_data,
                    'cmt': cmt_data,
                    'bgn': bgn_lines  
                }
                capturing_data = False
                data = []
                att_data = {}
                cmt_data = {}
                bgn_lines = []  
                print(f"Found EOT section for table '{current_table_name}'.")
            elif capturing_data:
                # Capture data rows only after 'BGN' line and before 'EOT'
                row_data = {headers[index]: value.strip() for index, value in enumerate(line[1:])}
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

def validate_tables(tables):
    # Perform validation on all tables
    for table_name, table_data in tables.items():
        if 'data' not in table_data or len(table_data['data']) == 0:
            print(f"Validation Error: Table '{table_name}' has no data or missing sections.")
            return False
        if 'headers' not in table_data or len(table_data['headers']) == 0:
            print(f"Validation Error: Table '{table_name}' is missing headers.")
            return False
        if 'att' not in table_data:
            print(f"Validation Error: Table '{table_name}' is missing attachment data.")
            return False
        if 'cmt' not in table_data:
            print(f"Validation Error: Table '{table_name}' is missing comment data.")
            return False
    return True


def export_to_tbe(tables, output_path):
    with open(output_path, 'w', newline='') as file:
        writer = csv.writer(file)
        
        for table_name, table_data in tables.items():
            # Write the table name and headers
            writer.writerow([f"TBL {table_name}"] + table_data['headers'])
            
            # Write original BGN lines as captured
            for bgn_line in table_data['bgn']:
                writer.writerow(bgn_line)
            
            # Write data rows
            for row in table_data['data']:
                writer.writerow([None] + list(row.values()))
            
            # Write EOT line with metadata
            writer.writerow([f"EOT {table_name}"] + [row[0] for row in table_data['data'][-1].items()])
            
            # Handle ATT and CMT sections
            if table_data['att']:
                for att_type, values in table_data['att'].items():
                    writer.writerow([f"ATT {att_type}"] + values)

            if table_data['cmt']:
                for cmt_type, values in table_data['cmt'].items():
                    writer.writerow([f"CMT {cmt_type}"] + values)

    print(f"Exported to {output_path} successfully.")

# Test the functionality with your file path
file_path = '../sample_data/saq_bluesky_npl_20220830_20230404_inv_tbe.csv'
tables = parse_tbe(file_path)

if tables and validate_tables(tables):
    print("All tables are valid.")
    # Export the tables to a new TBE file
    output_path = 'output_tbe_file.csv'
    export_to_tbe(tables, output_path)
else:
    print("Validation failed.")

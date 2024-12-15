use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead, BufReader};

#[derive(Debug, Default)]
pub struct Table {
    pub data: Vec<HashMap<String, String>>,     // Main table data
    pub att: HashMap<String, Vec<String>>,      // Attribute data linked to table
    pub cmt: HashMap<String, Vec<String>>,      // Comment data linked to table
}

pub fn parse_tbe(file_path: &str) -> io::Result<HashMap<String, Table>> {
    let file = File::open(file_path)?;
    let reader = BufReader::new(file);

    let mut tables: HashMap<String, Table> = HashMap::new();
    let mut current_table_name = String::new();
    let mut headers: Vec<String> = Vec::new();
    let mut capturing_data = false;

    for line in reader.lines() {
        let line = line?;
        let line = line.trim();

        // Handle table section
        if line.starts_with("TBL") {
            let parts: Vec<&str> = line.split(',').collect();
            if parts.len() > 1 {
                current_table_name = parts[0].split_whitespace().nth(1).unwrap_or_default().to_string();
                headers = parts.iter().skip(1).map(|s| s.trim().to_string()).collect();
                
                println!("Parsed table: {} with headers: {:?}", current_table_name, headers); // Debug log
                tables.entry(current_table_name.clone()).or_insert_with(Table::default);
            }
        }
        // Start reading table data
        else if line.starts_with("BGN") {
            capturing_data = true;
        }
        // End of table data
        else if line.starts_with("EOT") {
            capturing_data = false;
        }
        // Handle ATT (Attribute) section
        else if line.starts_with("ATT") {
            let parts: Vec<&str> = line.split(',').collect();
            if parts.len() > 2 {
                let att_name = parts[1].trim().to_string();
                let att_values: Vec<String> = parts.iter().skip(2).map(|s| s.trim().to_string()).collect();

                if let Some(table) = tables.get_mut(&current_table_name) {
                    table.att.insert(att_name, att_values);
                }
            }
        }
        // Handle CMT (Comment) section
        else if line.starts_with("CMT") {
            let parts: Vec<&str> = line.split(',').collect();
            if parts.len() > 2 {
                let cmt_name = parts[1].trim().to_string();
                let cmt_values: Vec<String> = parts.iter().skip(2).map(|s| s.trim().to_string()).collect();

                if let Some(table) = tables.get_mut(&current_table_name) {
                    table.cmt.insert(cmt_name, cmt_values);
                }
            }
        }
        // Parse table rows
        else if capturing_data {
            let parts: Vec<&str> = line.split(',').collect();
            if parts.len() == headers.len() {
                let row_data: HashMap<String, String> = headers
                    .iter()
                    .zip(parts.iter().map(|s| s.trim().to_string()))
                    .map(|(h, v)| (h.clone(), v))
                    .collect();

                // Push the cloned row into the table and log the captured row
                if let Some(table) = tables.get_mut(&current_table_name) {
                    table.data.push(row_data.clone()); // Clone to avoid moving
                    println!("Captured row: {:?}", row_data); // Debug log
                }
            } else {
                eprintln!("Skipping malformed row: {:?}", parts); // Debug log for malformed rows
            }
        }
    }

    Ok(tables)
}
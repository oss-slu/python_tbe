library(jsonlite)  # For JSON output
library(dplyr)     # For data manipulation
library(readr)     # For fast CSV reading
library(lubridate) # For working with dates and times

# Function to detect table sections and attributes
detect_table_sections_and_attributes <- function(data) {
  sections <- list()
  
  # Heuristic: Detect table sections based on patterns in column names or specific markers
  section_markers <- which(grepl("Section|Header", names(data), ignore.case = TRUE))
  
  if (length(section_markers) > 0) {
    for (marker in section_markers) {
      section_name <- names(data)[marker]
      section_data <- data[, marker, drop = FALSE]
      
      sections[[section_name]] <- list(
        attribute_names = colnames(section_data),
        row_count = nrow(section_data),
        column_count = ncol(section_data)
      )
    }
  } else {
    sections[["default"]] <- list(
      attribute_names = colnames(data),
      row_count = nrow(data),
      column_count = ncol(data)
    )
  }
  
  return(sections)
}

# Function to extract detailed column metadata
extract_column_metadata <- function(data) {
  metadata <- list(
    column_names = as.character(data[1, ]),  # Assuming first row contains column names
    att_units = as.character(data[2, ]),    # Assuming second row contains ATT Units
    att_description = as.character(data[3, ]),  # Assuming third row contains ATT Description
    att_displayname = as.character(data[4, ])   # Assuming fourth row contains ATT DisplayName
  )
  
  # Filter out NA or blank entries if necessary
  metadata <- lapply(metadata, function(row) {
    row[!is.na(row) & row != ""]
  })
  
  return(metadata)
}

# Parse function with column metadata extraction
parse_csv_with_metadata <- function(file_path) {
  tryCatch({
    cat("Processing file:", file_path, "\n")
    
    # Read the CSV with the first few rows to capture metadata
    preview_data <- read_csv(file_path, n_max = 10, show_col_types = FALSE, col_names = FALSE)
    
    # Extract column metadata
    column_metadata <- extract_column_metadata(preview_data)
    
    # Read full file, skipping metadata rows
    csv_data <- read_csv(file_path, skip = 4, show_col_types = FALSE)  # Assuming first 4 rows are metadata
    
    # Combine file and column metadata
    metadata <- list(
      creation_time = format(Sys.time(), "%Y-%m-%dT%H:%M:%OSZ"),
      last_modified_time = format(file.info(file_path)$mtime, "%Y-%m-%dT%H:%M:%OSZ"),
      file_name = basename(file_path),
      row_count = nrow(csv_data),
      column_count = ncol(csv_data),
      column_metadata = column_metadata
    )
    
    return(metadata)
  }, error = function(e) {
    message(paste("Error processing file:", file_path, "\n", e$message))
    return(NULL)
  })
}

# Main function to process files
process_csv_directory_with_metadata <- function(directory_path) {
  all_files <- list.files(directory_path, full.names = TRUE)
  csv_files <- all_files[grepl("\\.csv$", all_files)]
  
  if (length(csv_files) == 0) {
    stop("No CSV files found in the specified directory.")
  }
  
  all_metadata <- list()
  
  for (file_path in csv_files) {
    cat("Processing file:", file_path, "\n")
    result <- parse_csv_with_metadata(file_path)
    if (!is.null(result)) {
      all_metadata <- append(all_metadata, list(result))
    }
  }
  
  json_summary <- toJSON(all_metadata, pretty = TRUE)
  cat("Summary Metadata:\n", json_summary, "\n")
  return(json_summary)
}

# Specify directory
directory_path <- "./sample_data"

# Process files
result <- process_csv_directory_with_metadata(directory_path)

library(jsonlite)  # For JSON output
library(dplyr)     # For data manipulation
library(readr)     # For fast CSV reading

# Function to clean up a row and detect column headers
clean_row_for_header <- function(row) {
  # Remove any extra whitespace and NA values
  cleaned_row <- trimws(row)  # Trim whitespace from all elements
  cleaned_row[cleaned_row == ""] <- NA  # Replace empty strings with NA
  
  # If a row has no NA values, it could be the header row
  return(all(!is.na(cleaned_row)))
}

# Function to dynamically read the first few rows to detect column headers
parse_csv_file <- function(file_path) {
  tryCatch({
    # Print the file path for debugging
    cat("Processing file:", file_path, "\n")
    
    # Read the first 20 rows to preview and detect header row
    preview_data <- read_csv(file_path, n_max = 100, show_col_types = FALSE, col_names = FALSE)
    
    # Iterate through the preview data to detect where the header row is
    header_row <- NULL
    for (i in 1:nrow(preview_data)) {
      if (clean_row_for_header(preview_data[i,])) {
        header_row <- i
        break
      }
    }
    
    if (is.null(header_row)) {
      stop("Unable to detect header row in the file:", file_path)
    }
    
    # Read the full file again with the correct header row, starting at the header row
    csv_data <- read_csv(file_path, skip = header_row - 1, show_col_types = FALSE)
    
    # Extract metadata: file name, file size, record count, and column names
    metadata <- list(
      file_name = basename(file_path),
      file_size = file.info(file_path)$size,
      record_count = nrow(csv_data),
      column_names = paste(colnames(csv_data), collapse = ", ")  # Concatenate column names into a single string
    )
    
    # Return parsed data and metadata
    return(list(data = csv_data, metadata = metadata))
    
  }, error = function(e) {
    message(paste("Error reading file:", file_path, "\n", e$message))
    return(NULL)
  })
}

# Main function to process the CSV files in a directory
process_csv_directory <- function(directory_path) {
  # Get list of all files in the directory (including full file path)
  all_files <- list.files(directory_path, full.names = TRUE)
  
  # Filter for CSV files only
  csv_files <- all_files[grepl("\\.csv$", all_files)]
  
  # Initialize variables to store processed data and metadata
  all_data <- list()  # To store data frames from each file
  all_metadata <- data.frame()  # To store metadata for each file
  
  # Check if there are CSV files to process
  if (length(csv_files) == 0) {
    stop("No CSV files found in the specified directory.")
  }
  
  # Process each CSV file only once
  for (file_path in csv_files) {
    cat("Processing file:", file_path, "\n")
    
    # Parse the CSV file and extract data and metadata
    result <- parse_csv_file(file_path)
    
    if (!is.null(result)) {
      # Store parsed data and metadata
      all_data[[file_path]] <- result$data
      all_metadata <- bind_rows(all_metadata, as.data.frame(result$metadata))
    }
  }
  
  # Handle non-CSV files (if needed)
  non_csv_files <- all_files[!grepl("\\.csv$", all_files)]
  if (length(non_csv_files) > 0) {
    warning(paste("Non-CSV files found and skipped:", paste(non_csv_files, collapse = ", ")))
  }
  
  # Check if any data was processed
  if (length(all_data) == 0) {
    stop("No valid CSV files were processed.")
  }
  
  # Return summary in JSON format
  json_summary <- toJSON(all_metadata, pretty = TRUE)
  cat("Summary Metadata:\n", json_summary, "\n")
  
  # Print and Return data and metadata
  print("Returning the results with data and summary:")
  return(list(data = all_data, metadata_summary = all_metadata, json_summary = json_summary))
}

# Set the directory path to your 'sample_data' folder relative to your R script
directory_path <- "./sample_data"  # Relative path to the folder with CSV files

# Call the function to process the CSV files
result <- process_csv_directory(directory_path)
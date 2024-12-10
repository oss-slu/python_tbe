# Install the jsonlite package if you haven't installed it yet
# install.packages("jsonlite")
library(jsonlite)

strip_header <- function(filename) {
  # Attempt to read the file
  file_lines <- tryCatch(readLines(filename), error = function(e) NULL)
  
  # If file can't be read, return NULL
  if (is.null(file_lines)) {
    stop("Error opening file")
  }
  
  metadata <- list()  # Initialize an empty list to store metadata
  is_first_line <- TRUE  # Flag to skip the first line (header row)
  
  # Iterate through each line in the file
  for (line in file_lines) {
    # Trim newline character (R will typically handle this)
    line <- trimws(line)
    
    # Skip the first line (header row)
    if (is_first_line) {
      is_first_line <- FALSE
      next
    }
    
    # Stop parsing if we reach the "TBL Sites" section
    if (startsWith(line, "TBL Sites")) {
      break
    }
    
    # Split the line by comma
    tokens <- strsplit(line, ",")[[1]]
    
    # Ensure there are at least 3 tokens (Key, Value, and some possible extra fields)
    if (length(tokens) < 3) {
      next  # Skip invalid lines
    }
    
    # Extract key and value
    key <- tokens[2]
    value <- tokens[3]
    
    # Skip invalid lines (empty key or value)
    if (nchar(key) == 0 || nchar(value) == 0) {
      next
    }
    
    # Add key-value pair to the metadata list
    metadata[[key]] <- value
  }
  
  # If no metadata was found, issue a warning
  if (length(metadata) == 0) {
    warning("No header detected in the file")
  }
  
  # Convert the metadata list to JSON format
  metadata_json <- toJSON(metadata, pretty = TRUE)
  
  return(metadata_json)
}

# Directory containing the sample files
folder_path <- "sample_data"

# Get the list of all CSV files in the directory
csv_files <- list.files(folder_path, pattern = "\\.csv$", full.names = TRUE)

# Process each CSV file and generate its metadata
for (file in csv_files) {
  cat("Processing file:", file, "\n")
  metadata <- strip_header(file)
  
  # Print metadata for the file
  cat(metadata, "\n\n")
}

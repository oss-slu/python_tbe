#include "tbe_batch_processor.h"
#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <stdlib.h>

// Function to process a single TBE file
void process_tbe_file(const char* filepath, TBE_Metadata* metadata) {
    FILE* file = fopen(filepath, "r");
    if (!file) {
        printf("Error: Could not open file %s\n", filepath);
        metadata->is_processed = 0;
        return;
    }

    // Example: Parse and count lines
    metadata->record_count = 0;
    while (!feof(file)) {
        char line[1024];
        if (fgets(line, sizeof(line), file)) {
            metadata->record_count++;
        }
    }
    fclose(file);
    metadata->is_processed = 1;
}

// Function to process all TBE files in a directory
void process_tbe_directory(const char* dirpath) {
    DIR* dir = opendir(dirpath);
    struct dirent* entry;
    int total_records = 0;
    int processed_files = 0;

    if (!dir) {
        printf("Error: Could not open directory %s\n", dirpath);
        return;
    }

    while ((entry = readdir(dir)) != NULL) {
        // Only process files ending with "_tbe.csv"
        if (strstr(entry->d_name, "_tbe.csv")) {
            TBE_Metadata metadata;
            snprintf(metadata.filename, sizeof(metadata.filename), "%s/%s", dirpath, entry->d_name);
            process_tbe_file(metadata.filename, &metadata);

            if (metadata.is_processed) {
                printf("Processed %s: %d records\n", metadata.filename, metadata.record_count);
                total_records += metadata.record_count;
                processed_files++;
            }
        } else {
            printf("Skipped non-TBE file: %s\n", entry->d_name);
        }
    }
    closedir(dir);

    printf("\nSummary:\n");
    printf("Processed files: %d\n", processed_files);
    printf("Total records: %d\n", total_records);
}

// Function to generate a simple metadata summary
void generate_metadata_summary() {
    // Example: Print a placeholder for metadata summary
    printf("Metadata summary generation not fully implemented.\n");
    printf("This function can be expanded to aggregate more specific metadata.\n");
}

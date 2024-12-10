#include "tbe_batch_processor.h"
#include <stdio.h>
#include <string.h>
#include <dirent.h>
#include <stdlib.h>

// Aggregate structure for metadata
typedef struct {
    int total_files;        // Total files encountered
    int processed_files;    // Successfully processed files
    int skipped_files;      // Skipped files
    int total_records;      // Total records across all files
} Aggregate_Metadata;

Aggregate_Metadata aggregate = {0}; // Initialize to zero

// Function to process a single TBE file
void process_tbe_file(const char* filepath, TBE_Metadata* metadata) {
    FILE* file = fopen(filepath, "r");
    if (!file) {
        printf("Error: Could not open file %s\n", filepath);
        metadata->is_processed = 0;
        aggregate.skipped_files++;
        return;
    }

    // Parse and count lines
    metadata->record_count = 0;
    char line[1024];
    while (fgets(line, sizeof(line), file)) {
        metadata->record_count++;
    }
    fclose(file);

    metadata->is_processed = 1;
    aggregate.total_records += metadata->record_count;
    aggregate.processed_files++;
}

// Function to process all TBE files in a directory
void process_tbe_directory(const char* dirpath) {
    DIR* dir = opendir(dirpath);
    struct dirent* entry;

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
            }
        } else {
            printf("Skipped non-TBE file: %s\n", entry->d_name);
            aggregate.skipped_files++;
        }
    }
    closedir(dir);

    aggregate.total_files = aggregate.processed_files + aggregate.skipped_files;

    // Print a summary to the console
    printf("\nSummary:\n");
    printf("Processed files: %d\n", aggregate.processed_files);
    printf("Skipped files: %d\n", aggregate.skipped_files);
    printf("Total files: %d\n", aggregate.total_files);
    printf("Total records: %d\n", aggregate.total_records);

    if (aggregate.processed_files > 0) {
        printf("Average records per file: %.2f\n", (double)aggregate.total_records / aggregate.processed_files);
    }
}

// Function to generate metadata summary
void generate_metadata_summary() {
    printf("\nGenerating metadata summary...\n");
    printf("Processed files: %d\n", aggregate.processed_files);
    printf("Skipped files: %d\n", aggregate.skipped_files);
    printf("Total files: %d\n", aggregate.total_files);
    printf("Total records: %d\n", aggregate.total_records);

    if (aggregate.processed_files > 0) {
        printf("Average records per file: %.2f\n", (double)aggregate.total_records / aggregate.processed_files);
    }

    printf("Metadata summary generation complete.\n");
}

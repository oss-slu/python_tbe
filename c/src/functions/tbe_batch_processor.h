#ifndef TBE_BATCH_PROCESSOR_H
#define TBE_BATCH_PROCESSOR_H

#include <stdio.h>
#include <dirent.h>

// Metadata structure for TBE files
typedef struct {
    char filename[256];
    int record_count;
    int is_processed;
} TBE_Metadata;

// Functions for processing TBE files and directories
void process_tbe_file(const char* filepath, TBE_Metadata* metadata);
void process_tbe_directory(const char* dirpath);
void print_metadata_summary();

#endif

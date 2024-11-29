#ifndef TBE_BATCH_PROCESSOR_H
#define TBE_BATCH_PROCESSOR_H

#include <stdio.h>
#include <dirent.h>

typedef struct {
    char filename[256];
    int record_count;
    int is_processed;
} TBE_Metadata;

void process_tbe_file(const char* filepath, TBE_Metadata* metadata);
void process_tbe_directory(const char* dirpath);
void generate_metadata_summary();

#endif
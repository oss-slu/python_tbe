#include "functions/tbe_batch_processor.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <directory_to_process> [--summary]\n", argv[0]);
        return 1;
    }

    if (argc == 2 && strcmp(argv[1], "--summary") == 0) {
        // Generate JSON summary only
        generate_metadata_summary();
        printf("JSON summary file generated as 'metadata_summary.json'.\n");
        return 0;
    }

    const char* dirpath = argv[1];
    process_tbe_directory(dirpath);

    return 0;
}

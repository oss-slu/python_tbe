#include "functions/tbe_batch_processor.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage: %s <directory_to_process>\n", argv[0]);
        return 1;
    }

    const char* dirpath = argv[1];
    process_tbe_directory(dirpath);

    return 0;
}

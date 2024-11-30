#include "../include/tbe_header_parser.h"

int main() {
    const char* filename = "sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv";
    TBEHeader* header = parse_tbe_header(filename);

    if (header) {
        print_tbe_header(header);
        free_tbe_header(header);
    }
    else {
        fprintf(stderr, "Failed to parse TBE header.\n");
    }

    return 0;
}

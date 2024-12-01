#include "../include/tbe_header_parser.h"
#include "../include/tbe_header_writer.h"

int main() {
    const char* input_filename = "sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv";
    const char* output_filename = "c_tbe/output_data/exported_tbe.csv";

    // Parse the TBE header
    TBEHeader* header = parse_tbe_header(input_filename);

    if (header) {
        // Print the parsed header
        print_tbe_header(header);

        // Export the header back to the TBE format
        if (export_tbe_header(header, output_filename) == 0) {
            printf("TBE header exported successfully to %s.\n", output_filename);
        }
        else {
            fprintf(stderr, "Failed to export TBE header.\n");
        }

        // Free allocated memory
        free_tbe_header(header);
    }
    else {
        fprintf(stderr, "Failed to parse TBE header.\n");
    }

    return 0;
}

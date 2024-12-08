## isolate_header

This module parses the TBE file and isolates the header information, including global metadata (BGN and EOT attributes) and TBL sections.

### Features:
- **BGN Attributes**: Extracts metadata from the "BGN" section, storing key-value pairs.
- **TBL Sections**: Extracts attributes from each "TBL" section, associating them with the corresponding section name.
- **EOT Attributes**: Extracts metadata from the "EOT" section, similar to BGN.
- **Error Handling**: Handles empty lines, malformed entries, and unknown line types gracefully.
- **Utilities**: Includes helper functions for stripping quotes, splitting CSV lines, and trimming newline characters.

### Functions:
- `parse_TBE_header(const char* filename)`: Parses a TBE file and returns a structured `TBEHeader` object.
- `free_tbe_header(TBEHeader* header)`: Frees memory allocated for a `TBEHeader` object.
- `print_tbe_header(const TBEHeader* header)`: Outputs the parsed header structure for debugging purposes.

---

## output_csv

(Add your content here)

## output_TBE

(Add your content here)

## read_directory

(Add your content here)

## read_TBE

(Add your content here)

## strip_header

(Add your content here)

## unit_tests

(Add your content here)

## validate_TBE

(Add your content here)

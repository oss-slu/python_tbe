#ifndef TBE_HEADER_PARSER_H
#define TBE_HEADER_PARSER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define maximum lengths for names and values
#define MAX_NAME_LEN 256
#define MAX_VALUE_LEN 512

// Structure for a key-value pair (used for global metadata)
typedef struct Attribute {
    char name[MAX_NAME_LEN];
    char value[MAX_VALUE_LEN];
    struct Attribute* next;
} Attribute;

// Structure for a TBL section
typedef struct TBLSection {
    char name[MAX_NAME_LEN];
    Attribute* attributes;
    struct TBLSection* next;
} TBLSection;

// Structure for the entire TBE header
typedef struct TBEHeader {
    Attribute* bgn_attributes;    // Global metadata before TBL sections
    Attribute* eot_attributes;    // Global metadata after TBL sections
    TBLSection* sections;         // Linked list of TBL sections
} TBEHeader;

// Function prototypes
TBEHeader* parse_tbe_header(const char* filename);
void free_tbe_header(TBEHeader* header);
void print_tbe_header(const TBEHeader* header);

#endif // TBE_HEADER_PARSER_H

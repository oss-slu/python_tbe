#ifndef TBE_HEADER_H
#define TBE_HEADER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define constants for maximum lengths
#define MAX_NAME_LEN 256
#define MAX_VALUE_LEN 1024

// Structure to hold an attribute (ATT)
typedef struct Attribute {
    char name[MAX_NAME_LEN];
    char value[MAX_VALUE_LEN];
    struct Attribute* next; // Pointer to the next attribute in the linked list
} Attribute;

// Structure to hold a TBL section
typedef struct TBLSection {
    char name[MAX_NAME_LEN];       // Name of the TBL section
    Attribute* attributes;         // Linked list of attributes for this section
    struct TBLSection* next;       // Pointer to the next TBL section
} TBLSection;

// Structure to represent the entire TBE header
typedef struct TBEHeader {
    TBLSection* sections;          // Linked list of TBL sections
} TBEHeader;

// Function prototypes
TBEHeader* parse_tbe_header(const char* filename);
void free_tbe_header(TBEHeader* header);
void print_tbe_header(const TBEHeader* header);

#endif // TBE_HEADER_H

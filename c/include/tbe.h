#ifndef TBE_H
#define TBE_H

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#define MAX_NAME_LEN 256
#define MAX_VALUE_LEN 256

// Attribute structure
typedef struct Attribute {
    char name[MAX_NAME_LEN];
    char value[MAX_VALUE_LEN];
    struct Attribute* next;
} Attribute;

// TBL Section structure
typedef struct TBLSection {
    char name[MAX_NAME_LEN];
    Attribute* attributes;
    struct TBLSection* next;
} TBLSection;

// TBE Header structure
typedef struct TBEHeader {
    Attribute* bgn_attributes;
    Attribute* eot_attributes;
    TBLSection* sections;
} TBEHeader;

// Function prototypes
TBEHeader* parse_TBE_header(const char* filename);
void free_tbe_header(TBEHeader* header);
void print_tbe_header(const TBEHeader* header);
int export_TBE(const TBEHeader* header, const char* filename);
void add_attribute(Attribute** head, const char* name, const char* value);

#endif // TBE_H

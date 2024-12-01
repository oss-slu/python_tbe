#include "../include/tbe_header_parser.h"

// Helper function to add an attribute to a linked list
static void add_attribute(Attribute** head, const char* name, const char* value) {
    Attribute* new_attr = malloc(sizeof(Attribute));
    if (!new_attr) {
        perror("Memory allocation failed for Attribute");
        exit(EXIT_FAILURE);
    }
    strncpy(new_attr->name, name, MAX_NAME_LEN - 1);
    new_attr->name[MAX_NAME_LEN - 1] = '\0';
    strncpy(new_attr->value, value, MAX_VALUE_LEN - 1);
    new_attr->value[MAX_VALUE_LEN - 1] = '\0';
    new_attr->next = NULL;

    if (!*head) {
        *head = new_attr;
    }
    else {
        Attribute* current = *head;
        while (current->next) current = current->next;
        current->next = new_attr;
    }
}

TBEHeader* parse_tbe_header(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Error opening TBE file");
        return NULL;
    }

    TBEHeader* header = malloc(sizeof(TBEHeader));
    if (!header) {
        perror("Memory allocation failed for TBEHeader");
        fclose(file);
        return NULL;
    }
    header->bgn_attributes = NULL;
    header->eot_attributes = NULL;
    header->sections = NULL;
    TBLSection* current_section = NULL;

    char line[2048]; // Buffer for reading lines
    int line_number = 0;
    int in_bgn_section = 0;
    int in_eot_section = 0;

    while (fgets(line, sizeof(line), file)) {
        line_number++;
        // Remove newline characters
        line[strcspn(line, "\r\n")] = '\0';
        if (strlen(line) == 0) continue;   // Skip empty lines

        // Tokenize the line
        char* tokens[50];
        int token_count = 0;
        char* token = strtok(line, ",");
        while (token && token_count < 50) {
            tokens[token_count++] = token;
            token = strtok(NULL, ",");
        }

        if (token_count == 0) {
            fprintf(stderr, "Warning [Line %d]: Empty or invalid line encountered.\n", line_number);
            continue;
        }

        // Skip header line if present
        if (line_number == 1 && strncmp(tokens[0], "TBL", 3) == 0) {
            continue; // Assume first line is a header
        }

        // Handle BGN section
        if (strncmp(tokens[0], "BGN", 3) == 0) {
            in_bgn_section = 1;
            in_eot_section = 0;
            if (token_count >= 3) {
                add_attribute(&header->bgn_attributes, tokens[1], tokens[2]);
            }
            else if (token_count == 2) {
                add_attribute(&header->bgn_attributes, tokens[1], "");
            }
            else {
                fprintf(stderr, "Warning [Line %d]: BGN line missing key or value.\n", line_number);
            }
            continue;
        }

        // Handle EOT section
        if (strncmp(tokens[0], "EOT", 3) == 0) {
            in_eot_section = 1;
            in_bgn_section = 0;
            if (token_count >= 3) {
                add_attribute(&header->eot_attributes, tokens[1], tokens[2]);
            }
            else if (token_count == 2) {
                add_attribute(&header->eot_attributes, tokens[1], "");
            }
            else {
                fprintf(stderr, "Warning [Line %d]: EOT line missing key or value.\n", line_number);
            }
            continue;
        }

        // Handle continuation lines for BGN and EOT
        if (in_bgn_section || in_eot_section) {
            if (token_count >= 3) {
                Attribute** attr_list = in_bgn_section ? &header->bgn_attributes : &header->eot_attributes;
                add_attribute(attr_list, tokens[1], tokens[2]);
            }
            else if (token_count == 2) {
                Attribute** attr_list = in_bgn_section ? &header->bgn_attributes : &header->eot_attributes;
                add_attribute(attr_list, tokens[1], "");
            }
            else {
                fprintf(stderr, "Warning [Line %d]: Continuation line missing key or value.\n", line_number);
            }
            continue;
        }

        // Handle TBL sections
        if (strncmp(tokens[0], "TBL", 3) == 0) {
            if (token_count >= 2) {
                TBLSection* new_section = malloc(sizeof(TBLSection));
                if (!new_section) {
                    perror("Memory allocation failed for TBLSection");
                    fclose(file);
                    free_tbe_header(header);
                    return NULL;
                }
                strncpy(new_section->name, tokens[1], MAX_NAME_LEN - 1);
                new_section->name[MAX_NAME_LEN - 1] = '\0';
                new_section->attributes = NULL;
                new_section->next = NULL;

                if (!header->sections) {
                    header->sections = new_section;
                }
                else {
                    TBLSection* last_section = header->sections;
                    while (last_section->next) last_section = last_section->next;
                    last_section->next = new_section;
                }
                current_section = new_section;
            }
            else {
                fprintf(stderr, "Warning [Line %d]: TBL section missing name.\n", line_number);
            }
            continue;
        }

        // Handle ATT lines
        if (strncmp(tokens[0], "ATT", 3) == 0) {
            if (!current_section) {
                fprintf(stderr, "Warning [Line %d]: ATT line encountered without an active TBL section.\n", line_number);
                continue;
            }
            for (int i = 1; i < token_count; i++) {
                if (strlen(tokens[i]) == 0) {
                    fprintf(stderr, "Warning [Line %d]: Empty attribute name in ATT line.\n", line_number);
                    continue;
                }
                // Check if there's a corresponding value
                char* value = "";
                if (i + 1 < token_count) {
                    value = tokens[i + 1];
                    i++; // Skip the value in the next token
                }
                add_attribute(&current_section->attributes, tokens[i], value);
            }
            continue;
        }

        // Handle data lines or unknown lines
        fprintf(stderr, "Warning [Line %d]: Unknown line type '%s' encountered. Skipping.\n", line_number, tokens[0]);
    }

    fclose(file);
    return header;
}

void free_tbe_header(TBEHeader* header) {
    if (!header) return;

    // Free BGN attributes
    Attribute* attr = header->bgn_attributes;
    while (attr) {
        Attribute* next_attr = attr->next;
        free(attr);
        attr = next_attr;
    }

    // Free EOT attributes
    attr = header->eot_attributes;
    while (attr) {
        Attribute* next_attr = attr->next;
        free(attr);
        attr = next_attr;
    }

    // Free TBL sections and their attributes
    TBLSection* section = header->sections;
    while (section) {
        Attribute* section_attr = section->attributes;
        while (section_attr) {
            Attribute* next_attr = section_attr->next;
            free(section_attr);
            section_attr = next_attr;
        }
        TBLSection* next_section = section->next;
        free(section);
        section = next_section;
    }

    free(header);
}

void print_tbe_header(const TBEHeader* header) {
    if (!header) {
        printf("No header to display.\n");
        return;
    }

    printf("=== Global Metadata (BGN) ===\n");
    const Attribute* attr = header->bgn_attributes;
    while (attr) {
        printf("  %s: %s\n", attr->name, attr->value);
        attr = attr->next;
    }
    printf("\n");

    printf("=== Global Metadata (EOT) ===\n");
    attr = header->eot_attributes;
    while (attr) {
        printf("  %s: %s\n", attr->name, attr->value);
        attr = attr->next;
    }
    printf("\n");

    const TBLSection* section = header->sections;
    while (section) {
        printf("TBL Section: %s\n", section->name);
        const Attribute* section_attr = section->attributes;
        while (section_attr) {
            printf("  Attribute: %s = %s\n", section_attr->name, section_attr->value);
            section_attr = section_attr->next;
        }
        section = section->next;
        printf("\n");
    }
}

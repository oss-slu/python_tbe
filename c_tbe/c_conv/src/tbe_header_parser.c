#include "../include/tbe_header_parser.h"

TBEHeader* parse_tbe_header(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Error opening TBE file");
        return NULL;
    }

    TBEHeader* header = malloc(sizeof(TBEHeader));
    if (!header) {
        perror("Memory allocation failed");
        fclose(file);
        return NULL;
    }
    header->sections = NULL;
    TBLSection* current_section = NULL;

    char line[2048]; // Buffer for reading lines
    while (fgets(line, sizeof(line), file)) {
        line[strcspn(line, "\r\n")] = '\0'; // Remove newline characters
        if (strlen(line) == 0) continue;   // Skip empty lines

        char* tokens[50];
        int token_count = 0;
        char* token = strtok(line, ",");
        while (token && token_count < 50) {
            tokens[token_count++] = token;
            token = strtok(NULL, ",");
        }

        if (token_count == 0) {
            fprintf(stderr, "Warning: Empty or invalid line encountered.\n");
            continue;
        }

        if (strncmp(tokens[0], "TBL", 3) == 0) {
            if (token_count < 1) {
                fprintf(stderr, "Warning: TBL section missing name.\n");
                continue;
            }

            TBLSection* new_section = malloc(sizeof(TBLSection));
            if (!new_section) {
                perror("Memory allocation failed");
                fclose(file);
                return NULL;
            }
            strncpy(new_section->name, tokens[0] + 4, MAX_NAME_LEN); // Remove 'TBL ' prefix
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
        else if (strncmp(tokens[0], "ATT", 3) == 0) {
            if (!current_section) {
                fprintf(stderr, "Warning: ATT line encountered without an active TBL section.\n");
                continue;
            }

            for (int i = 1; i < token_count; i++) {
                if (strlen(tokens[i]) == 0) {
                    fprintf(stderr, "Warning: Empty attribute name in ATT line.\n");
                    continue;
                }

                Attribute* new_attr = malloc(sizeof(Attribute));
                if (!new_attr) {
                    perror("Memory allocation failed");
                    fclose(file);
                    return NULL;
                }
                strncpy(new_attr->name, tokens[i], MAX_NAME_LEN);
                new_attr->value[0] = '\0'; // Initialize value to empty
                new_attr->next = NULL;

                if (!current_section->attributes) {
                    current_section->attributes = new_attr;
                }
                else {
                    Attribute* last_attr = current_section->attributes;
                    while (last_attr->next) last_attr = last_attr->next;
                    last_attr->next = new_attr;
                }
            }
        }
        else {
            fprintf(stderr, "Warning: Unknown line type '%s' encountered. Skipping.\n", tokens[0]);
        }
    }

    fclose(file);
    return header;
}

void free_tbe_header(TBEHeader* header) {
    TBLSection* section = header->sections;
    while (section) {
        Attribute* attr = section->attributes;
        while (attr) {
            Attribute* next_attr = attr->next;
            free(attr);
            attr = next_attr;
        }
        TBLSection* next_section = section->next;
        free(section);
        section = next_section;
    }
    free(header);
}

void print_tbe_header(const TBEHeader* header) {
    const TBLSection* section = header->sections;
    while (section) {
        printf("TBL Section: %s\n", section->name);
        const Attribute* attr = section->attributes;
        while (attr) {
            printf("  Attribute: %s = %s\n", attr->name, attr->value);
            attr = attr->next;
        }
        section = section->next;
        printf("\n");
    }
}

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 1024
#define MAX_ROWS 1000
#define MAX_ATT 100
#define MAX_CMT 100

// Structures
typedef struct
{
    char *data[MAX_ROWS];
    int rows;
} TBLData;

typedef struct
{
    char *attributes[MAX_ATT];
    int count;
} ATTData;

typedef struct
{
    char *comments[MAX_CMT];
    int count;
} CMTData;

typedef struct
{
    char header[MAX_LINE_LENGTH];
    TBLData tblData;
    ATTData attData;
    CMTData cmtData;
} TBEFile;

// Function Prototypes
void parse_tbe_file(const char *filename, TBEFile *tbe);
void print_tbe_file(const TBEFile *tbe);
char **split_line_into_array(const char *line, int *numCols);
char *trim_whitespace(char *str);

// Helper Function: Trim whitespace
char *trim_whitespace(char *str)
{
    char *end;
    while (*str == ' ')
        str++; // Trim leading spaces
    if (*str == '\0')
        return str; // All spaces
    end = str + strlen(str) - 1;
    while (end > str && *end == ' ')
        end--; // Trim trailing spaces
    *(end + 1) = '\0';
    return str;
}

// Main Function
int main()
{
    TBEFile tbe = {0};
    const char *filename = "../../sample_data/saq_bluesky_npl_20220830_20230404_inv_tbe.csv";

    parse_tbe_file(filename, &tbe);
    print_tbe_file(&tbe);

    // Free dynamically allocated memory
    for (int i = 0; i < tbe.tblData.rows; i++)
    {
        free(tbe.tblData.data[i]);
    }
    for (int i = 0; i < tbe.attData.count; i++)
    {
        free(tbe.attData.attributes[i]);
    }
    for (int i = 0; i < tbe.cmtData.count; i++)
    {
        free(tbe.cmtData.comments[i]);
    }

    return 0;
}

// Function to parse TBE files
void parse_tbe_file(const char *filename, TBEFile *tbe)
{
    FILE *file = fopen(filename, "r");
    if (!file)
    {
        perror("Error opening file");
        return;
    }

    char line[MAX_LINE_LENGTH];
    int in_tbl = 0, in_att = 0;

    while (fgets(line, sizeof(line), file))
    {
        char *trimmed = trim_whitespace(line);

        // Detect Section Start
        if (strncmp(trimmed, "TBL", 3) == 0)
        {
            in_tbl = 1;
            in_att = 0;
            strncpy(tbe->header, trimmed + 4, sizeof(tbe->header));
            tbe->header[sizeof(tbe->header) - 1] = '\0'; // Ensure null termination
        }
        else if (strncmp(trimmed, "ATT", 3) == 0)
        {
            in_tbl = 0;
            in_att = 1;
        }
        else if (strncmp(trimmed, "CMT", 3) == 0)
        {
            in_tbl = 0;
            in_att = 0;
            if (tbe->cmtData.count < MAX_CMT)
            {
                tbe->cmtData.comments[tbe->cmtData.count++] = strdup(trimmed + 4);
            }
        }
        else if (strncmp(trimmed, "EOT", 3) == 0)
        {
            // Include EOT rows in both TBL and ATT sections
            if (in_tbl && tbe->tblData.rows < MAX_ROWS)
            {
                tbe->tblData.data[tbe->tblData.rows++] = strdup(trimmed);
            }
            if (in_att && tbe->attData.count < MAX_ATT)
            {
                tbe->attData.attributes[tbe->attData.count++] = strdup(trimmed);
            }
            in_tbl = 0;
            in_att = 0;
        }
        else
        {
            // Store data within the section
            if (in_tbl && tbe->tblData.rows < MAX_ROWS)
            {
                tbe->tblData.data[tbe->tblData.rows++] = strdup(trimmed);
            }
            else if (in_att && tbe->attData.count < MAX_ATT)
            {
                tbe->attData.attributes[tbe->attData.count++] = strdup(trimmed);
            }
        }
    }

    fclose(file);
}

void print_tbe_file(const TBEFile *tbe)
{
    printf("\n=== TBE File Data ===\n");

    // TBL Section
    printf("\nTBL Section:\n");
    printf("----------------------------------------------------\n");
    printf("%-20s%-20s%-40s\n", "TBL Global", "Variable", "Value");
    printf("----------------------------------------------------\n");

    for (int i = 0; i < tbe->tblData.rows; i++)
    {
        int numCols = 0;
        char **columns = split_line_into_array(tbe->tblData.data[i], &numCols);

        if (numCols > 0)
        {
            if (strcmp(columns[0], "BGN") == 0 || strcmp(columns[0], "EOT Global") == 0 || strcmp(columns[0], "EOT Timeseries") == 0)
            {
                printf("%-20s", columns[0]);
                if (numCols > 1)
                {
                    printf("%-20s%-40s\n", columns[1], (numCols > 2 ? columns[2] : ""));
                }
                else
                {
                    printf("\n");
                }
            }
            else
            {
                printf("%-20s", "");
                for (int j = 0; j < numCols; j++)
                {
                    printf("%-20s", columns[j]);
                }
                printf("\n");
            }
        }

        for (int j = 0; j < numCols; j++)
        {
            free(columns[j]);
        }
        free(columns);
    }

    printf("----------------------------------------------------\n");

    printf("\nATT Section:\n");
    printf("----------------------------------------------------\n");

    // Print ATT Header
    printf("%-20s%-15s%-25s%-20s%-20s%-10s%-15s%-15s%-10s%-15s%-10s%-20s%-20s%-20s%-15s%-15s%-15s%-15s\n",
           "ATT DisplayName", "Country", "Sitename", "Site ID", "Serial Number",
           "Plocation", "Latitude", "Longitude", "Is Indoors", "Measurements",
           "Records", "Start Date", "End Date", "Timezone", "UTC Offset",
           "PM25 Calib", "PM25 Scale", "PM25 Offset");

    printf("----------------------------------------------------\n");

    for (int i = 0; i < tbe->attData.count; i++)
    {
        int numCols = 0;
        char **columns = split_line_into_array(tbe->attData.attributes[i], &numCols);

        // Print all columns in order
        for (int j = 0; j < numCols; j++)
        {
            // Ensure proper alignment for the first column (ATT DisplayName)
            if (strcmp(columns[0], "BGN") == 0 || strcmp(columns[0], "EOT Timeseries") == 0)
            {
                printf("%-20s", columns[j]); // "BGN", "EOT Timeseries", or blank
            }
            else
            {
                printf("%-20s", "");

                printf("%-20s", columns[j]);
            }
        }
        printf("\n");

        // Free memory for columns
        for (int j = 0; j < numCols; j++)
        {
            free(columns[j]);
        }
        free(columns);
    }

    printf("----------------------------------------------------\n");

    // CMT Section
    printf("\nCMT Section:\n");
    printf("----------------------------------------------------\n");
    for (int i = 0; i < tbe->cmtData.count; i++)
    {
        printf("%s\n", tbe->cmtData.comments[i]);
    }
    printf("----------------------------------------------------\n");

    printf("\n=== End of TBE File Data ===\n");
}

// Helper Function to split rows into columns
char **split_line_into_array(const char *line, int *numCols)
{
    char *lineCopy = strdup(line);
    char *token;
    char **columns = malloc(sizeof(char *) * 100); // Allocate space for up to 100 columns
    *numCols = 0;

    token = strtok(lineCopy, ","); // Split by comma
    while (token != NULL)
    {
        columns[*numCols] = strdup(token); // Store each column
        (*numCols)++;
        token = strtok(NULL, ",");
    }

    free(lineCopy); // Free temporary copy of line
    return columns;
}

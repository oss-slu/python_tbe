package Maven;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.json.JSONArray;
import org.json.JSONObject;

public class ReadDirectory {

    private static final Logger logger = Logger.getLogger(ReadDirectory.class.getName());

    public static void main(String[] args) {
        // Define directory path and output file path
        String directoryPath = "../../sample_data";
        String outputFilePath = "Read_directory_metadata.json";

        try {
            // Validate the input directory path
            validateDirectory(directoryPath);

            // Process TBE files in the directory
            JSONArray summary = processCSVFiles(directoryPath);

            // Export metadata summary to a JSON file
            exportSummaryToFile(summary, outputFilePath);

            // Print the summary in JSON format to the console
            System.out.println("Metadata Summary: \n" + summary.toString(4));

            // Additional visualization option: Print a table (for console)
            printMetadataAsTable(summary);
        } catch (IOException e) {
            logger.log(Level.SEVERE, "Error while processing files: {0}", e.getMessage());
        }
    }

    /**
     * Validates the directory path to ensure it exists and is accessible.
     *
     * @param directoryPath The path of the directory to validate.
     * @throws IllegalArgumentException If the directory is invalid.
     */
    private static void validateDirectory(String directoryPath) {
        Path dirPath = Paths.get(directoryPath);
        if (!Files.exists(dirPath) || !Files.isDirectory(dirPath)) {
            throw new IllegalArgumentException("Invalid directory path: " + directoryPath);
        }
    }

    /**
     * Processes all CSV files in the specified directory and aggregates metadata.
     *
     * @param directoryPath The path of the directory to process.
     * @return JSONArray containing aggregated metadata for each CSV file.
     * @throws IOException If there is an error accessing the directory or files.
     */
    public static JSONArray processCSVFiles(String directoryPath) throws IOException {
        JSONArray summary = new JSONArray();

        // Iterate over files in the directory
        Files.list(Paths.get(directoryPath)).forEach(filePath -> {
            if (Files.isRegularFile(filePath) && filePath.toString().endsWith(".csv")) {
                try {
                    logger.log(Level.INFO, "Processing file: {0}", filePath.getFileName());
                    JSONObject metadata = extractMetadata(filePath.toFile());
                    summary.put(metadata);
                } catch (IOException e) {
                    logger.log(Level.WARNING, "Failed to process file: {0} - Reason: {1}",
                            new Object[]{filePath.getFileName(), e.getMessage()});
                }
            } else if (Files.isRegularFile(filePath)) {
                logger.log(Level.WARNING, "Skipping non-CSV file: {0}", filePath.getFileName());
            }
        });

        return summary;
    }

    /**
     * Extracts metadata from a CSV file.
     *
     * @param file The CSV file to extract metadata from.
     * @return A JSONObject containing metadata key-value pairs.
     * @throws IOException If there is an error reading the file or its attributes.
     */
    private static JSONObject extractMetadata(File file) throws IOException {
        JSONObject metadata = new JSONObject();
        Path filePath = file.toPath();
        BasicFileAttributes attr = Files.readAttributes(filePath, BasicFileAttributes.class);

        metadata.put("file_name", file.getName());
        metadata.put("file_size", attr.size());
        metadata.put("creation_time", attr.creationTime().toString());
        metadata.put("last_modified_time", attr.lastModifiedTime().toString());

        if (file.getName().endsWith(".csv")) {
            List<String> lines = Files.readAllLines(filePath);
            metadata.put("row_count", lines.size() - 1); // Subtract header row
            if (!lines.isEmpty()) {
                String[] columns = lines.get(0).split(",");
                metadata.put("column_count", columns.length);
                metadata.put("column_names", new JSONArray(columns));
                metadata.put("sample_data", new JSONArray(lines.subList(1, Math.min(6, lines.size())))); // First 5 rows
            }
        }
        return metadata;
    }

    /**
     * Exports the metadata summary to a JSON file.
     *
     * @param summary        The metadata summary to export.
     * @param outputFilePath The path of the output JSON file.
     * @throws IOException If there is an error writing the file.
     */
    private static void exportSummaryToFile(JSONArray summary, String outputFilePath) throws IOException {
        try (FileWriter fileWriter = new FileWriter(outputFilePath)) {
            fileWriter.write(summary.toString(4)); // Pretty print JSON with indentation
        }
        logger.log(Level.INFO, "Metadata summary exported to: {0}", outputFilePath);
    }

    /**
     * Prints metadata in a tabular format to the console.
     *
     * @param summary JSONArray containing the metadata summary.
     */
    private static void printMetadataAsTable(JSONArray summary) {
        System.out.printf("%-30s %-10s %-30s %-30s%n", "File Name", "Rows", "Columns", "Column Names");
        System.out.println("=".repeat(100));

        for (int i = 0; i < summary.length(); i++) {
            JSONObject metadata = summary.getJSONObject(i);
            System.out.printf("%-30s %-10d %-30d %-30s%n",
                    metadata.getString("file_name"),
                    metadata.optInt("row_count", 0),
                    metadata.optInt("column_count", 0),
                    metadata.getJSONArray("column_names").toString());
        }
    }
}

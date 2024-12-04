package Maven;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.List;
import java.util.logging.Logger;

import org.json.JSONArray;
import org.json.JSONObject;

public class ReadDirectory {

    private static final Logger logger = Logger.getLogger(ReadDirectory.class.getName());

    public static void main(String[] args) {
        String directoryPath = "../../sample_data";
        String outputFilePath = "Read_directory_metadata.json";

        try {
            // Process TBE files in the directory
            JSONArray summary = processTBEFiles(directoryPath);

            // Export metadata summary to a JSON file
            exportSummaryToFile(summary, outputFilePath);

            // Print the summary to the console
            System.out.println("Metadata Summary: \n" + summary.toString(4));
        } catch (IOException e) {
            logger.severe("Error while processing files: " + e.getMessage());
        }
    }

    /**
     * Processes all TBE files in the specified directory and aggregates metadata.
     *
     * @param directoryPath The path of the directory to process.
     * @return JSONArray containing aggregated metadata for each TBE file.
     * @throws IOException If there is an error accessing the directory or files.
     */
    public static JSONArray processTBEFiles(String directoryPath) throws IOException {
        Path dirPath = Paths.get(directoryPath);
        if (!Files.exists(dirPath) || !Files.isDirectory(dirPath)) {
            throw new IllegalArgumentException("Invalid directory path: " + directoryPath);
        }

        JSONArray summary = new JSONArray();
        Files.list(dirPath).forEach(filePath -> {
            if (Files.isRegularFile(filePath) && filePath.toString().endsWith(".csv")) {
                try {
                    logger.info("Processing file: " + filePath.getFileName());
                    JSONObject metadata = extractMetadata(filePath.toFile());
                    summary.put(metadata);
                } catch (Exception e) {
                    logger.warning("Failed to process file: " + filePath.getFileName() + " - " + e.getMessage());
                }
            } else if (Files.isRegularFile(filePath)) {
                logger.warning("Skipping non-TBE file: " + filePath.getFileName());
            }
        });

        return summary;
    }

    /**
     * Extracts metadata from a TBE file.
     *
     * @param file The TBE file to extract metadata from.
     * @return A JSONObject containing metadata key-value pairs.
     * @throws IOException If there is an error reading the file or its attributes.
     */
    private static JSONObject extractMetadata(File file) throws IOException {
        JSONObject metadata = new JSONObject();
        
        Path filePath = file.toPath();
        BasicFileAttributes attr = Files.readAttributes(filePath, BasicFileAttributes.class);

        metadata.put("file_name", file.getName());  // File name
        metadata.put("file_size", attr.size());    // File size in bytes
        metadata.put("creation_time", attr.creationTime().toString());  // File creation time
        metadata.put("last_modified_time", attr.lastModifiedTime().toString());  // Last modified time
        
        if (file.getName().endsWith(".csv")) {
        List<String> lines = Files.readAllLines(filePath);
        metadata.put("row_count", lines.size() - 1);
        if (!lines.isEmpty()) {
            String[] columns = lines.get(0).split(",");
            metadata.put("column_count", columns.length);
            metadata.put("column_names", new JSONArray(columns));
            if (lines.size() > 1) {
                metadata.put("sample_data", new JSONArray(lines.subList(1, Math.min(5, lines.size()))));
            }
        }
    }
        return metadata;
    }

    /**
     * Exports the metadata summary to a JSON file.
     *
     * @param summary      The metadata summary to export.
     * @param outputFilePath The path of the output JSON file.
     * @throws IOException If there is an error writing the file.
     */
    private static void exportSummaryToFile(JSONArray summary, String outputFilePath) throws IOException {
        try (FileWriter fileWriter = new FileWriter(outputFilePath)) {
            fileWriter.write(summary.toString(4)); // Pretty print JSON with indentation
        }
        logger.info("Metadata summary exported to: " + outputFilePath);
    }
}

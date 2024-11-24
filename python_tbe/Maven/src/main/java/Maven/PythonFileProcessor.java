package  Maven;

import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.logging.*;
import org.json.JSONObject;

public class PythonFileProcessor {

    private static final Logger logger = Logger.getLogger(PythonFileProcessor.class.getName());

    public static void main(String[] args) {
        String directoryPath = "C:\\Users\\ajith\\OneDrive\\Desktop\\Project DOC\\tbe\\python_tbe\\python_conv";
        String outputFilePath = "python_metadata_summary.json";

        try {
            // Process Python files in the directory
            JSONObject summary = processPythonDirectory(directoryPath);

            // Export metadata summary to a JSON file
            exportSummaryToFile(summary, outputFilePath);

            // Print the summary to the console
            System.out.println("Metadata Summary: \n" + summary.toString(4));
        } catch (IOException e) {
            logger.severe("Error while processing files: " + e.getMessage());
        }
    }

    /**
     * Processes all Python files in the specified directory and aggregates metadata.
     *
     * @param directoryPath The path of the directory to process.
     * @return JSONObject containing aggregated metadata.
     * @throws IOException If there is an error accessing the directory or files.
     */
    public static JSONObject processPythonDirectory(String directoryPath) throws IOException {
        Path dirPath = Paths.get(directoryPath);
        if (!Files.exists(dirPath) || !Files.isDirectory(dirPath)) {
            throw new IllegalArgumentException("Invalid directory path: " + directoryPath);
        }

        JSONObject summary = new JSONObject();
        Files.list(dirPath).forEach(filePath -> {
            if (Files.isRegularFile(filePath) && filePath.toString().endsWith(".py")) {
                try {
                    logger.info("Processing file: " + filePath.getFileName());
                    Map<String, String> metadata = parsePythonFile(filePath.toFile());
                    summary.put(filePath.getFileName().toString(), metadata);
                } catch (Exception e) {
                    logger.warning("Failed to process file: " + filePath.getFileName() + " - " + e.getMessage());
                }
            } else if (Files.isRegularFile(filePath)) {
                logger.warning("Skipping non-Python file: " + filePath.getFileName());
            }
        });

        return summary;
    }

    /**
     * Parses a Python file to extract metadata.
     *
     * @param file The Python file to parse.
     * @return A map containing metadata key-value pairs.
     * @throws IOException If there is an error reading the file.
     */
    private static Map<String, String> parsePythonFile(File file) throws IOException {
        Map<String, String> metadata = new HashMap<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                // Extract metadata from Python comments (e.g., lines starting with #)
                if (line.startsWith("#")) {
                    line = line.substring(1).trim(); // Remove the # and trim
                    if (line.contains(":")) {
                        String[] parts = line.split(":", 2);
                        metadata.put(parts[0].trim(), parts[1].trim());
                    }
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
    private static void exportSummaryToFile(JSONObject summary, String outputFilePath) throws IOException {
        try (FileWriter fileWriter = new FileWriter(outputFilePath)) {
            fileWriter.write(summary.toString(4)); // Pretty print JSON with indentation
        }
        logger.info("Metadata summary exported to: " + outputFilePath);
    }
}

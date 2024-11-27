package java_tbe;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.*;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.io.File;

public class LoadTBEFile {

    public void loadTBEFile() {

        String rootDir = System.getProperty("user.dir");

        String[] filePaths = {
                rootDir + File.separator + "sample_data" + File.separator
                        + "saq_bluesky_bgd_20211001_20230430_inv_tbe.csv",
                rootDir + File.separator + "sample_data" + File.separator
                        + "saq_bluesky_dku_20210715_20230131_inv_tbe.csv",
                rootDir + File.separator + "sample_data" + File.separator
                        + "saq_bluesky_npl_20220830_20230404_inv_tbe.csv"
        };
        List<Map<String, String>> rows = new ArrayList<>();

        try {
            for (String filePath : filePaths) {
                InputStream inputStream = new FileInputStream(filePath);
                BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
                String line = reader.readLine();
                String[] headers = null;
                while (line != null) {
                    line = line.replace("\"", "");
                    if (line != null && line.startsWith("TBL Sites")) {
                        headers = line.split(",");
                        for (int i = 0; i < headers.length; i++) {
                            headers[i] = headers[i].trim();
                        }
                        reader.readLine();
                        reader.readLine();
                        reader.readLine();
                    }
                    if (line != null && line.startsWith("TBL Sites")) {
                        // reader.readLine(); // ATT Units
                        // reader.readLine(); // ATT Description
                        // reader.readLine(); // ATT DisplayName
                        while ((line = reader.readLine()) != null) {
                            line = line.replace("\"", "");
                            if (/* line.startsWith("BGN") */true) {
                                // Split the row by commas to get values
                                String[] values = line.split(",");
                                Map<String, String> row = new LinkedHashMap<>();

                                // Populate the map with the header as key and corresponding value
                                for (int i = 1; i < headers.length && i < values.length; i++) {
                                    String value = values[i].trim();
                                    if (value.isEmpty()) {
                                        value = "NULL"; // Handle missing values as "NULL" or any other placeholder
                                    }
                                    row.put(headers[i], value);
                                }
                                rows.add(row);
                                // System.out.println("rows : " + row);
                            }
                        }
                    }
                    line = reader.readLine();

                }
                reader.close();
            }
            System.out.println("rows : " + rows);
        } catch (Exception e) {
            System.out.println("Error is : " + e);
        }

    }

    public static void main(String[] args) {
        LoadTBEFile loadTBEFileObj = new LoadTBEFile();
        loadTBEFileObj.loadTBEFile();
    }
}
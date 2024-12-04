import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.*;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.io.File;

public class Read_TBE {

    public void loadTBEFile() {

        String rootDir = System.getProperty("user.dir");
        File root = new File(rootDir);
        File projectRoot = root.getParentFile().getParentFile().getParentFile();

        String[] filePaths = {

                projectRoot + File.separator + "sample_data" + File.separator
                        + "saq_bluesky_bgd_20211001_20230430_inv_tbe.csv",
                projectRoot + File.separator + "sample_data" + File.separator
                        + "saq_bluesky_dku_20210715_20230131_inv_tbe.csv",
                projectRoot + File.separator + "sample_data" + File.separator
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
                        while ((line = reader.readLine()) != null) {
                            line = line.replace("\"", "");
                            String[] values = line.split(",");
                            Map<String, String> row = new LinkedHashMap<>();
                            for (int i = 1; i < headers.length && i < values.length; i++) {
                                String value = values[i].trim();
                                if (value.isEmpty()) {
                                    value = "NULL";
                                }
                                row.put(headers[i], value);
                            }
                            rows.add(row);
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
        Read_TBE loadTBEFileObj = new Read_TBE();
        loadTBEFileObj.loadTBEFile();
    }
}
mod functions; // Include the functions module
use functions::read_tbe::parse_tbe; // Import the parse_tbe function

use std::io; // Import io for Result
use std::path::PathBuf; // Import PathBuf for path management

mod models;  // Import models where the Site struct is defined


fn main() -> io::Result<()> {
    let file_path = PathBuf::from("../sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv"); // Path to the sample TBE file
    // let file_path = PathBuf::from("../sample_data/saq_bluesky_dku_20210715_20230131_inv_tbe.csv"); // Path to the sample TBE file
    // let file_path = PathBuf::from("../sample_data/saq_bluesky_npl_20220830_20230404_inv_tbe.csv"); // Path to the sample TBE file
    println!("Parsing TBE file: {}", file_path.display()); // Use .display() to print the PathBuf

    let result = parse_tbe(file_path.to_str().unwrap());

    match result {
        Ok(sites) => {
            // Now sites is a vector of `Site` structs
            for site in sites {
                println!("{:?}", site); // Print each site
            }
        }
        Err(e) => eprintln!("Error parsing file: {}", e),
    }

    Ok(())
}
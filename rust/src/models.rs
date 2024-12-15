// models.rs
// use serde_derive::Deserialize; // Add the import for the macro

#[allow(dead_code)] 
pub struct Site {
    pub zone: String,
    pub country: String,
    pub sitename: String,
    pub utc_offset: String,
    pub pm25_scale: String,
    pub pm25_offset: String,
    pub serial_number: String,
    pub plocation: String,
    pub latitude: String,
    pub longitude: String,
    pub is_indoors: String,
    pub measurements: String,
    pub nrecords: String,
    pub date_start: String,
    pub date_end: String,
    pub time: String,
}
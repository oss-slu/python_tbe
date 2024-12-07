# TBE File Processing Suite

A multi-language toolkit for handling TBE (Tabular Data with Metadata Blocks and Enrichment) files. This suite includes libraries 
in Python, C, Rust, R, JavaScript, and Java, designed for flexible use by both programmers and data analysts. Each language-specific
library allows you to parse, validate, manipulate, and export data from TBE files, facilitating cross-functional collaboration in 
data-driven projects.

## Sample Data Files
This repository includes the following TBE sample data files:

- **saq_bluesky_bgd_20211001_20230430_inv_tbe.csv** - Contains inventory data for Bluesky BGD covering the period from October 1, 2021, to April 30, 2023.
- **saq_bluesky_dku_20210715_20230131_inv_tbe.csv** - Contains inventory data for Bluesky DKU from July 15, 2021, to January 31, 2023.
- **saq_bluesky_npl_20220830_20230404_inv_tbe.csv** - Contains inventory data for Bluesky NPL from August 30, 2022, to April 4, 2023.

These files are used as sample data to demonstrate the TBE file structure and test the TBE Processing Suite functionalities.

## What is TBE?

TBE files are metadata-enriched tabular files that contain multiple structured "TBL" sections. Each section includes a unique 
name, column headers, and rows of data, with optional attributes and comments. TBE files use specific control markers (BGN, EOT) to 
define sections and organize data.
#### TBE Structure Overview
- **TBL:** A table-like data section with a unique name, column headers, and data rows.
- **ATT:** Optional attributes for TBL sections, represented as key-value pairs or lists.
- **CMT:** Comments associated with TBL sections.
- **Control Codes:** Specific codes within the first column indicate the start and end of sections (BGN, EOT).

## Tech Stack
- **JavaScript:** TBE Validator Tool – a JavaScript CLI tool to check structural and content compliance of TBE files.
- **Python:** TBE Library – a Python package enabling easy parsing, validation, and metadata aggregation of TBE files.
- **R:** TBE Library – an R package for statistical and tabular analysis of TBE files, ideal for research and analytics.
- **C:** TBE Library – a high-performance C library for file parsing, validation, and efficient data handling.
- **Java:** TBE Library – a Java package for enterprise applications to load, process, and validate TBE data.
- **Rust:** TBE Library – a Rust library optimized for fast parsing and validation of TBE files.

## Architecture
Each library is designed to meet the specific needs of its target environment while adhering to a common TBE file standard, enabling 
consistent cross-platform handling of TBE data.

## Coding Standards

This project uses multiple programming languages. Below are the coding standards for each:

- [C Coding Standards](./C_Coding_Standards.md)
- [Java Coding Standards](./Java_Coding_Standards.md)
- [R Coding Standards](./R_Coding_Standards.md)
- [JavaScript Coding Standards](./JavaScript_Coding_Standards.md)
- [Python Coding Standards](./Python_Coding_Standards.md)
- [Ruby Coding Standards](./Ruby_Coding_Standards.md)


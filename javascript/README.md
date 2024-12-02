
# **JavaScript TBE Metadata Processor**

This project provides a JavaScript utility for processing TBE (Tabular Data with Metadata Blocks and Enrichment) files, extracting metadata, and returning it in a structured JSON format. The utility reads all files in a specified directory, filters for TBE files, and processes their metadata dynamically.

## **Table of Contents**
- [Project Overview](#project-overview)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Directory Structure](#directory-structure)

## **Project Overview**
This utility allows users to efficiently read and process TBE files within a directory. It:
- Filters files to process only `.tbe` files.
- Dynamically extracts metadata from TBE files.
- Returns the extracted metadata in a JSON format, making it easier for users to work with TBE file data without needing to process the entire file.

## **Installation**
### Prerequisites
- Ensure that you have [Node.js](https://nodejs.org/) installed.

### Steps to Install
1. Clone the repository:
   ```bash
   git clone https://github.com/oss-slu/tbe
   ```
2. Navigate to the project directory:
   ```bash
   cd project-name
   ```
3. Install dependencies: (No dependencies for this feature besides the prerequisite Node JS, skip step if node is installed)
   ```bash
   npm install
   ```

## **Usage**
### To Read TBE Files and Out Processed Metadata as JSON:
1. Place your TBE files in the `sample_data/` directory (or specify a directory path).
2. Run the `read_TBE.js` script:
   ```bash
   node read_TBE.js
   ```

The script will read all `.tbe` files in the specified directory, extract metadata, and log it in the console as a JSON object.

## **Contributing**
### How to Contribute
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes.
4. Push your branch to your fork and create a pull request.

Please ensure that your code follows the project's conventions and includes tests where applicable.


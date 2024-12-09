## Installation

Follow these steps to install the necessary dependencies for the project:

```bash
npm install
```

## isolate_header

(Add your content here)

## output_csv

(Add your content here)

## output_TBE

The main function of src/functions/readTBE.js, parseTBE() returns a JSON object, tables. outputTBE() takes in two parameters, a file path to write to, and a JSON object representing the tbe tables. The function writes the data within the JSON tables object to a .csv file with proper tbe formatting. Simply run ```node outputTBE.js ./path-to-file/output-file-name.csv``` from the directory containing the function (currently /javascript/src/functions).

Following the example usage outlined in the file, the resulting .csv looks like
TBL Users,Name,Age,Country
BGN,Alice,25,USA
Bob,30,Canada
EOT Charlie,22,UK
ATT Info,Active,Verified
CMT Notes,Test User,New

## read_directory

### To Read TBE Files and Out Processed Metadata as JSON:
1. Place your TBE files in the `sample_data/` directory (or specify a directory path).
2. Run the `readDirectory.js` script:
   ```bash
   node readDirectory.js
   ```

The script will read all `.tbe` files in the specified directory, extract metadata, and log it in the console as a JSON object.

## read_TBE

To start parsing sample TBE files into JavaScript native objects, you can use one of the following commands:

```bash
npm run start-readTBE
```
or

```bash
node src/functions/readTBE
```

## strip_header
# Steps to run the application.

* Change directory to javascript
* Run <code>npm install</code>
* Update the file path in <code>javascript/demo/parse-header.js</code> - line7
* Run <code>npm run start-stripHeader</code>


## unit_tests

(Add your content here)

## validate_TBE

(Add your content here)

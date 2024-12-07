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

(Add your content here)

## read_TBE

(Add your content here)

## strip_header

(Add your content here)

## unit_tests

(Add your content here)

## validate_TBE

(Add your content here)

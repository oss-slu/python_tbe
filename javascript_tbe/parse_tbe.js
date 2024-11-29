const fs = require('fs');
const readline = require('readline');

async function parseTBE(filePath) {
    const stream = fs.createReadStream(filePath);
    const reader = readline.createInterface({ input: stream });

    const tables = {};
    let currentTableName = '';
    let capturingData = false;
    let headers = [];
    let data = [];
    let attData = {};
    let cmtData = {};

    for await (const line of reader) {
        if (line.startsWith('TBL')) {
            // Extract table name and headers from 'TBL' line
            const parts = line.split(',');
            const firstPart = parts[0].split(' ');
            currentTableName = firstPart[1].trim();
            headers = parts.slice(1).map(header => header.trim());
        } else if (line.startsWith('BGN')) {
            // Start capturing data after 'BGN'
            capturingData = true;

            // Capture data row
            const rowData = line.split(',').slice(1).reduce((obj, value, index) => {
                obj[headers[index]] = value.trim();
                return obj;
            }, {});
            data.push(rowData);
        } else if (line.startsWith('EOT')) {
            // Capture data row
            const rowData = line.split(',').slice(1).reduce((obj, value, index) => {
                obj[headers[index]] = value.trim();
                return obj;
            }, {});
            data.push(rowData);

            // Stop capturing data when 'EOT' is reached
            capturingData = false;
            // Add last set of data if any
            if (data.length > 0) {
                tables[currentTableName] = { data: data, att: attData, cmt: cmtData }
                // Reset all values for potential subsequent tables
                data = [];
                attData = {};
                cmtData = {}
            }
        } else if (capturingData) {
            // Capture data row
            const rowData = line.split(',').slice(1).reduce((obj, value, index) => {
                obj[headers[index]] = value.trim();
                return obj;
            }, {});
            data.push(rowData);
        } else if (line.startsWith('ATT')) {
            // Parse and store ATT data
            const parts = line.split(',')
            const type = parts[0].split(' ')[1];
            const attValues = parts.slice(1).map(value => value.trim());
            attData[type] = attValues;
        } else if (line.startsWith('CMT')) {
            // Parse and store CMT data
            const parts = line.split(',')
            const type = parts[0].split(' ')[1];
            const cmtValues = parts.slice(1).map(value => value.trim());
            cmtData[type] = cmtValues;
        }
    }

    return tables;
}

const filePath = '../sample_data/saq_bluesky_bgd_20211001_20230430_inv_tbe.csv';
parseTBE(filePath).then(tables => {
    // fs.writeFile('output.json', JSON.stringify(tables, null, 2), (err) => {
    //     if (err) {
    //         console.error('Error writing to JSON file', err);
    //     } else {
    //         console.log('Data successfully written to output.json');
    //     }
    // });
    
    console.log("Available Tables and Their Data:");
    for (const [tableName, tableData] of Object.entries(tables)) {
        console.log(`Table: ${tableName}`);
        console.table(tableData.data)
        console.log(tableData.att);
        console.log(tableData.cmt);
        console.log(`Table ${tableName} ends here.....`);
    }
}).catch(error => {
    console.error('Error parsing TBE file:', error);
});


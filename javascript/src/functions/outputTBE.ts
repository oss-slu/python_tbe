import { writeFile, mkdir } from 'fs/promises';
import path from 'path';

// parseTBE() returns tables object of type Tables
type TableData = {
    data: Array<Record<any, any>>;
    att: Record<any, any[]>;
    cmt: Record<any, any[]>;
}

type Tables = {
    [tableName: string]: TableData
}

/**
 * Outputs the TBE format for the given tables and writes it to a specified directory.
 *
 * @param directory - The directory where the output file will be written.
 * @param tables - An object containing table data, attributes, and comments.
 * @returns A promise that resolves when the file has been written.
 */
const outputTBE = async (directory: string, tables: Tables): Promise<void> => {
    let dataToWrite = ''

    // create the directory in case it does not exist
    const dir = path.dirname(directory);
    await mkdir(dir, { recursive: true });
    
    try{
        Object.keys(tables).forEach(table => {
            const headers = Object.keys(tables[table].data[0]).join(',')

            const allRows = tables[table].data.map(row => Object.values(row));
            const lastRow = allRows.pop()?.join(',')
            const rowData = allRows.map(row => row.join(',')).join('\n')

            const attData = Object.entries(tables[table].att)
            .map(([key, values]) => `${key},${values.join(',')}`)

            const cmtData = Object.entries(tables[table].cmt)
            .map(([key, values]) => `${key},${values.join(',')}`)

            dataToWrite += `TBL ${table},${headers}\nBGN,${rowData}\nEOT ${lastRow}\nATT ${attData}\nCMT ${cmtData}`
        })
        
        await writeFile(directory, dataToWrite);
    } catch(err) {
        throw err;
    }
};

// example usage
const testDirectory = process.argv[2] || './output.csv'

const exampleTables = {
    "Users": {
        "data": [
            { "Name": "Alice", "Age": "25", "Country": "USA" },
            { "Name": "Bob", "Age": "30", "Country": "Canada" },
            { "Name": "Charlie", "Age": "22", "Country": "UK" }
        ],
        "att": { "Info": ["Active", "Verified"] },
        "cmt": { "Notes": ["Test User", "New"] }
    }
}

outputTBE(testDirectory, exampleTables)

export default outputTBE;

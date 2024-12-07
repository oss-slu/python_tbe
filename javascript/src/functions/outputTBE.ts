import { writeFile } from 'fs/promises';

// parseTBE() returns tables object of type Tables
type TableData = {
    data: Array<Record<any, any>>;
    att: Record<any, any[]>;
    cmt: Record<any, any[]>;
}

type Tables = {
    [tableName: string]: TableData
}

const outputTBE = async (directory: string, tables: Tables): Promise<void> => {
    try{
        const dataToWrite = JSON.stringify(tables)
        await writeFile(directory, dataToWrite);
    } catch(err) {
        throw err;
    }
};

// example usage
// run ```node outputTBE.js ./my-custom-directory/output.csv```
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

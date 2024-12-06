import {writeFile} from 'node:fs';

/**
 * writes the tbe file to a specified user directory
 * @param {string} directory
 * @param {any} data
 * @returns {Promise<void>} resolves on successful write, rejects on error
 */
const outputTBE = (directory, data) => {
    return new Promise((resolve, reject) => {
        writeFile(directory, data, (err) => {
            if (err) {
                reject(err);
            } else {
                console.log(`The file has been saved at ${directory}!`);
                resolve();
            }
        });
    });
};

// example usage
// run ```node outputTBE.js ./my-custom-directory/output.csv```
const testDirectory = process.argv[2] || './output.csv'
const testData = 'column1,column2\nvalue1,value2'
outputTBE(testDirectory, testData)
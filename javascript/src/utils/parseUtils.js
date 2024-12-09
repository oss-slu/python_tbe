const fs = require('fs')
const path = require('path')

/**
 * Parses the metadata of a TBE file.
 */
async function parseTBEMetadata(filePath) {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                return reject(err)
            }

            const metadata = {
                filename: path.basename(filePath),
                size: data.length,
            }
            resolve(metadata)
        })
    })
}

module.exports = { parseTBEMetadata }
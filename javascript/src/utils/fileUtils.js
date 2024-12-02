const fs = require('fs')
const path = require('path')
const { parseTBEMetadata } = require('./parseUtils')

/**
 * Processes all TBE files in a directory, aggregates metadata, and generates a summary report.
 */
async function processTBEDirectory(directoryPath) {
    const metadataSummary = {}

    if (!fs.existsSync(directoryPath) || !fs.statSync(directoryPath).isDirectory()) {
        throw new Error("Provided path is not a valid directory")
    }

    const files = fs.readdirSync(directoryPath)

    for (const file of files) {
        const filePath = path.join(directoryPath, file)

        try {
            if (isTBEFile(filePath)) {
                console.log(`Processing file: ${file}`)

                const metadata = await parseTBEMetadata(filePath)
                metadataSummary[file] = metadata
            } else {
                console.warn(`Skipping non-TBE file: ${file}`)
            }
        } catch (error) {
            console.error(`Error processing file ${file}:`, error.message)
        }
    }

    return metadataSummary
}

/**
 * Checks if a file is a valid TBE file based on its extension.
 */
function isTBEFile(filePath) {
    const ext = path.extname(filePath).toLowerCase()
    return ext === '.tbe'
}

module.exports = { processTBEDirectory, isTBEFile }
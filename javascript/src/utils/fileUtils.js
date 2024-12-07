const fs = require('fs')
const path = require('path')
const { parseTBEMetadata } = require('./parseUtils')


/**
 * Processes all TBE files in a directory, aggregates metadata, and generates a summary report,
 * including the file content.
 */
async function processTBEDirectory(directoryPath) {
    const fileDetails = {}

    if (!fs.existsSync(directoryPath) || !fs.statSync(directoryPath).isDirectory()) {
        throw new Error("Provided path is not a valid directory")
    }

    const files = fs.readdirSync(directoryPath)

    for (const file of files) {
        const filePath = path.join(directoryPath, file)

        try {
            if (isTBEFile(filePath)) {
                console.log(`Processing file: ${file}`)

                // Read file content
                const content = fs.readFileSync(filePath, 'utf-8')

                // Parse metadata
                const metadata = await parseTBEMetadata(filePath)

                // Include content and metadata in the summary
                fileDetails[file] = {
                    metadata,
                    content
                }
            } else {
                console.warn(`Skipping non-TBE file: ${file}`)
            }
        } catch (error) {
            console.error(`Error processing file ${file}:`, error.message)
        }
    }

    return fileDetails
}

/**
 * Checks if a file is a valid TBE file based on its extension.
 */
function isTBEFile(filePath) {
    const ext = path.extname(filePath).toLowerCase()
    return ext === '.tbe'
}

module.exports = { processTBEDirectory, isTBEFile }
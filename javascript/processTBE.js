const { processTBEDirectory } = require('./utils/fileUtils');

(async () => {
    try {
        const directoryPath = '../sample_data'
        const summary = await processTBEDirectory(directoryPath)

        console.log("Summary of Metadata: ", JSON.stringify(summary, null, 2))
    } catch (error) {
        console.error("Error:", error.message)
    }
})()
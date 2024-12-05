const fs = require('fs');
const errorMessages = require('../constants/error-messages');

/**
 * Validates the input file before processing
 * @param {string} filePath - Path to the TBE file
 * @throws {Error} If file validation fails
 */
function validateFile(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(errorMessages.fileNotFound);
  }

  const stats = fs.statSync(filePath);

  if (stats.size === 0) {
    throw new Error(errorMessages.fileEmpty);
  }

  try {
    fs.accessSync(filePath, fs.constants.R_OK);
  } catch (error) {
    throw new Error(errorMessages.permissionDenied);
  }
}

module.exports = { validateFile };

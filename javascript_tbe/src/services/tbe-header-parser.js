const fs = require('fs');
const errorMessages = require('../constants/error-messages');
const warningMessages = require('../constants/warning-messages');
const { validateFile } = require('../utils/file-validator');

/**
 * @typedef {Object} ParserResponse
 * @property {string} status - 'success', 'warning', or 'error'
 * @property {Object} metadata - Extracted metadata or empty object
 * @property {string} [message] - Error or warning message
 * @property {string[]} [warnings] - Array of warning messages
 */

/**
 * Extracts global metadata from a TBE file
 * @param {string} filePath - Path to the TBE file
 * @returns {ParserResponse} Object containing metadata and status information
 */

function extractTbeHeader(filePath) {
  try {
    validateFile(filePath);

    const fileContent = fs.readFileSync(filePath,'utf-8');
    const lines = fileContent.split('\n');

    const metadata = {};
    let isGlobalSection = false;
    let headerFound = false;
    let previousLine = '';
    const warnings = [];

    for (const line of lines) {
      const trimmedLine = line.trim();
      
      if (trimmedLine === 'TBL Global,Variable,Value') {
        isGlobalSection = true;
        headerFound = true;
        continue;
      }
      
      if (trimmedLine.startsWith('TBL Sites')) {
        // Process the last EOT Global line before breaking
        if (previousLine && previousLine.startsWith('EOT Global')) {
          const parts = previousLine.split(',').map(part => part.trim());
          if (parts.length >= 3) {
            const key = parts[1];
            const value = parts[2];
            if (key && value) {
              metadata[key] = value;
            }
          }
        }
        break;
      }
      
      if (isGlobalSection && trimmedLine) {
        const parts = trimmedLine.split(',').map(part => part.trim());
        if (parts.length >= 3) {
          const key = parts[0] === 'BGN' ? parts[1] : parts[1];
          const value = parts[2];
          
          if (key && value) {
            metadata[key] = value;
          }
        }
      }

      previousLine = trimmedLine;
    }

    if (!headerFound) {
      return {
        status: 'warning',
        message: warningMessages.noHeader,
        metadata: {},
        warnings: [warningMessages.noHeader]
      };
    }

    return {
      status: warnings.length > 0 ? 'warning' : 'success',
      metadata,
      warnings: warnings.length > 0 ? warnings : undefined
    };

  } catch (error) {
    if (error.code === 'ENOENT') {
      return {
        status: 'error',
        message: errorMessages.fileNotFound,
        metadata: {}
      };
    }
    
    return {
      status: 'error',
      message: error.message || errorMessages.unexpectedError,
      metadata: {}
    };
  }
}
module.exports = { extractTbeHeader };

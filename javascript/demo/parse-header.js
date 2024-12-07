const { stripHeader } = require('../');

/**
 * This file is to test the tbe header parser with validations and header processing
 */
function demonstrateHeaderParsing() {
  const filePath = '../sample_data/saq_bluesky_dku_20210715_20230131_inv_tbe.csv';
  console.log(filePath)
  const result = stripHeader(filePath);
  
  switch (result.status) {
    case 'success':
      console.log('Successfully extracted metadata:');
      console.log(JSON.stringify(result.metadata, null, 2));
      break;
      
    case 'warning':
      console.log('Metadata extracted with warnings:');
      console.log('Warnings:', result.warnings);
      console.log('Metadata:', JSON.stringify(result.metadata, null, 2));
      break;
      
    case 'error':
      console.error('Failed to extract metadata:', result.message);
      break;
      
    default:
      console.error('Unexpected response status');
  }
}

// Execute if run directly
if (require.main === module) {
  demonstrateHeaderParsing();
}

module.exports = { demonstrateHeaderParsing };

const { stripHeader } = require('./src/functions/stripHeader');
const errorMessages = require('./src/constants/error-messages');
const warningMessages = require('./src/constants/warning-messages');

module.exports = {
  stripHeader,
  errorMessages,
  warningMessages
};

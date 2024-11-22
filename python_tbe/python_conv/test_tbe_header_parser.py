import unittest
from io import StringIO
import logging
from tbe_header_parser import parse_tbe_file, check_missing_metadata

class TestTBEParser(unittest.TestCase):
    def setUp(self):
        # Capture logging output
        self.log_stream = StringIO()
        logging.basicConfig(stream=self.log_stream, level=logging.WARNING)

    def test_parse_tbe_file_valid(self):
        # Simulate a valid TBE file (replace with the actual file or mock it)
        test_file = 'test_invalid_format_tbe.csv'
        metadata = parse_tbe_file(test_file)
        self.assertIn('Title', metadata)
        self.assertIn('Source', metadata)
        self.assertIn('TBL', metadata)

    def test_parse_tbe_file_missing_title(self):
        # Simulate a TBE file missing the 'Title' field
        test_file = 'test_missing_title_tbe.csv'
        metadata = parse_tbe_file(test_file)
        self.assertNotIn('Title', metadata)
        check_missing_metadata(metadata)

        # Verify the log captured the missing Title warning
        self.log_stream.seek(0)
        log_output = self.log_stream.read()
        self.assertIn("Missing required metadata field: 'Title'", log_output)


    def test_parse_tbe_file_duplicate_key(self):
        # Simulate a TBE file with duplicate keys in a TBL section
        test_file = 'test_duplicate_key_tbe.csv'
        metadata = parse_tbe_file(test_file)
        self.assertIn('Duplicate key', str(metadata))

        # Verify that the duplicate key warning was logged
        self.log_stream.seek(0)
        log_output = self.log_stream.read()
        self.assertIn("Duplicate key 'Title'", log_output)


    def test_parse_tbe_file_invalid_format(self):
        # Simulate a TBE file with invalid format (e.g., missing values)
        test_file = 'test_invalid_format_tbe.csv'
        metadata = parse_tbe_file(test_file)
        self.assertIsNone(metadata)

        # Check if invalid format was captured
        self.log_stream.seek(0)
        log_output = self.log_stream.read()
        self.assertIn("Unexpected row format", log_output)

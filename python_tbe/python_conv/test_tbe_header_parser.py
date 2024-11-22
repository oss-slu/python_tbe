import unittest
from tbe_header_parser import parse_tbe_file, check_missing_metadata

class TestTBEParser(unittest.TestCase):
    def test_parse_tbe_file_valid(self):
        # Simulate a valid TBE file (replace with the actual file or mock it)
        test_file = 'test_valid_tbe.csv'
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

    def test_parse_tbe_file_duplicate_key(self):
        # Simulate a TBE file with duplicate keys in a TBL section
        test_file = 'test_duplicate_key_tbe.csv'
        metadata = parse_tbe_file(test_file)
        self.assertIn('Duplicate key', str(metadata))

    def test_parse_tbe_file_invalid_format(self):
        # Simulate a TBE file with invalid format (e.g., missing values)
        test_file = 'test_invalid_format_tbe.csv'
        metadata = parse_tbe_file(test_file)
        self.assertIsNone(metadata)
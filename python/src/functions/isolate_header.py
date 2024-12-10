import csv
import re
from typing import Optional, List

class Attribute:
    def __init__(self, name: str, value: str):
        self.name = name.strip('"')
        self.value = value.strip('"')

    def __repr__(self):
        return f"{self.name}: {self.value}"

class TBLSection:
    def __init__(self, name: str):
        self.name = name.strip('"')
        self.attributes: List[Attribute] = []

    def add_attribute(self, name: str, value: str):
        self.attributes.append(Attribute(name, value))

    def __repr__(self):
        return f"TBL Section: {self.name}\n" + "\n".join(str(attr) for attr in self.attributes)

class TBEHeader:
    def __init__(self):
        self.bgn_attributes: List[Attribute] = []
        self.eot_attributes: List[Attribute] = []
        self.sections: List[TBLSection] = []

    def add_bgn_attribute(self, name: str, value: str):
        self.bgn_attributes.append(Attribute(name, value))

    def add_eot_attribute(self, name: str, value: str):
        self.eot_attributes.append(Attribute(name, value))

    def add_section(self, section: TBLSection):
        self.sections.append(section)

    def __repr__(self):
        return (
            "=== Global Metadata (BGN) ===\n" +
            "\n".join(str(attr) for attr in self.bgn_attributes) + "\n\n" +
            "=== Global Metadata (EOT) ===\n" +
            "\n".join(str(attr) for attr in self.eot_attributes) + "\n\n" +
            "\n".join(str(section) for section in self.sections)
        )

def trim_newline(line: str) -> str:
    return line.strip()

def split_csv_line(line: str) -> List[str]:
    """Splits a CSV line into tokens, handling quoted fields."""
    reader = csv.reader([line])
    return next(reader)

def parse_tbe_header(filename: str) -> Optional[TBEHeader]:
    header = TBEHeader()
    current_section: Optional[TBLSection] = None
    in_bgn_section = False
    in_eot_section = False

    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, 1):
                line = trim_newline(line)

                # Skip empty lines or delimiter-only lines
                if not line or all(c in ', ' for c in line):
                    continue

                tokens = split_csv_line(line)
                if not tokens:
                    continue

                # Handle section headers
                if tokens[0].startswith("BGN"):
                    in_bgn_section, in_eot_section = True, False
                    if len(tokens) >= 3:
                        header.add_bgn_attribute(tokens[1], tokens[2])
                    elif len(tokens) == 2:
                        header.add_bgn_attribute(tokens[1], "")
                elif tokens[0].startswith("EOT"):
                    in_bgn_section, in_eot_section = False, True
                    if len(tokens) >= 3:
                        header.add_eot_attribute(tokens[1], tokens[2])
                    elif len(tokens) == 2:
                        header.add_eot_attribute(tokens[1], "")
                elif tokens[0].startswith("TBL"):
                    in_bgn_section = in_eot_section = False
                    if len(tokens) >= 2:
                        current_section = TBLSection(tokens[1])
                        header.add_section(current_section)
                    else:
                        print(f"Warning [Line {line_number}]: TBL section missing name.")
                elif tokens[0].startswith("ATT"):
                    if current_section:
                        for i in range(1, len(tokens), 2):
                            name = tokens[i]
                            value = tokens[i + 1] if i + 1 < len(tokens) else ""
                            current_section.add_attribute(name, value)
                    else:
                        print(f"Warning [Line {line_number}]: ATT line without active TBL section.")
                elif in_bgn_section or in_eot_section:
                    if len(tokens) >= 3:
                        attr_list = header.bgn_attributes if in_bgn_section else header.eot_attributes
                        attr_list.append(Attribute(tokens[1], tokens[2]))
                    elif len(tokens) == 2:
                        attr_list = header.bgn_attributes if in_bgn_section else header.eot_attributes
                        attr_list.append(Attribute(tokens[1], ""))
                else:
                    print(f"Warning [Line {line_number}]: Unknown line type '{tokens[0]}'. Skipping.")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

    return header

# Example usage
if __name__ == "__main__":
    tbe_header = parse_tbe_header("example.tbe")
    if tbe_header:
        print(tbe_header)

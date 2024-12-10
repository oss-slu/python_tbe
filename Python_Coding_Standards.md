# Python Coding Standards

### General Best Practices
- Adhere to [PEP 8](https://peps.python.org/pep-0008/).
- Use snake_case for variables and function names.
- Write meaningful docstrings for all functions and classes using the PEP 257 convention.

### Code Formatting
- Use 4 spaces for indentation (no tabs).
- Limit lines to 79 characters, but it's acceptable to exceed this limit when:
  - Long URLs or import statements are involved.
  - Breaking the line would negatively impact readability.
- Place one blank line between functions and two between classes.

### Testing
- Use `pytest` for testing, and ensure tests cover both typical and edge cases.
- Name test functions with the test_ prefix (e.g., test_function_name) to ensure compatibility with pytest.
- Use mocks for external API calls or dependencies to isolate unit tests.
- Ensure to follow the respective library's README file to verify correct testing commands and functionality.

### Additional Guidelines
- Type annotate function arguments and return values.
- Use list comprehensions where appropriate for readability.

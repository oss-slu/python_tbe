# C Coding Standards

### General Best Practices
- Ensure all functions have a clear description of their purpose and parameter details.
- Include header guards in all `.h` files to prevent multiple inclusions.
- Limit the use of global variables; prefer `static` variables for internal module use.
- Maintain a soft limit of 100 characters per line for readability.
- Comment complex logic and non-intuitive code using `/* */` format.

### Code Formatting
- Indent with tabs (4 spaces equivalent).
- Place the opening brace `{` on the same line as the statement (K&R style).
- Use descriptive names for variables and functions, avoiding abbreviations.
- Declare variables at the beginning of blocks.

### Testing and Debugging
- Write unit tests for each function using a testing framework like CUnit.
- Use tools such as `Valgrind` to check for memory leaks.
- Check for `NULL` pointers before dereferencing.
- Ensure to follow the respective library's README file to verify correct testing commands and functionality.

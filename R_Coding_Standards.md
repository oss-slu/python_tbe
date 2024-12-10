# R Coding Standards

### General Best Practices
- Use meaningful names for variables, functions, and scripts.
- Avoid hardcoding file paths; use relative paths and configuration files.
- Comment statistical methods and dataset manipulations, especially when the logic is complex. Specify the technique or approach used, e.g., p-value calculation, confidence intervals, etc.
- Follow the tidyverse style guide for consistency across the codebase.

### Code Formatting
- Use 2 spaces for indentation (no tabs).
- Limit lines to 80 characters, but it’s acceptable to exceed this limit when:
  - Long URLs or file paths are involved.
  - Breaking the line would negatively impact readability.
- Place spaces around operators for clarity (e.g., x <- 10 instead of x<-10).
- Functions should be formatted with:
  - A space before the opening parenthesis for clarity (e.g., my_function(x, y)).
  - Consistent indentation and line breaks for arguments.

### Documentation
- Document functions using `roxygen2` format.
    - Include a detailed description of the function, its arguments, return values, and side effects.
- Include reproducible examples in function documentation, especially for complex operations or methods.

### Testing
- Use `testthat` for unit testing.
- Ensure coverage of edge cases in statistical calculations (e.g., handling of NA values, zero or negative values).
- Test function names should describe what the test is checking for (e.g., test_calculate_mean_correctly_handles_na()).
- Ensure to follow the respective library's README file to verify correct testing commands and functionality.

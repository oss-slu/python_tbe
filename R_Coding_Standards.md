# R Coding Standards

### General Best Practices
- Use meaningful names for variables, functions, and scripts.
- Avoid hardcoding file paths; use relative paths and configuration files.
- Add comments to explain statistical methods and dataset manipulations.
- Follow the tidyverse style guide for consistency.

### Code Formatting
- Use 2 spaces for indentation (no tabs).
- Limit lines to 80 characters.
- Place spaces around operators (e.g., `x <- 10` instead of `x<-10`).

### Documentation
- Document functions using `roxygen2` format.
- Include reproducible examples in function documentation.

### Testing
- Use `testthat` for unit testing.
- Ensure coverage of edge cases in statistical calculations.

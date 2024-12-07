# Ruby Coding Standards

### General Best Practices
- Follow the [Ruby Style Guide](https://rubystyle.guide/).
- Use descriptive method and variable names.
- Avoid monkey-patching core classes unless absolutely necessary.

### Code Formatting
- Indent using 2 spaces (no tabs).
- Use snake_case for variables and methods.
- Limit lines to 80 characters.

### Testing
- Write tests using RSpec.
- Group tests logically into describe/context blocks.
- Use FactoryBot for test data creation.

### Additional Guidelines
- Prefer single-line blocks (`{}`) for short operations and `do...end` for multi-line.
- Use `?` and `!` in method names where appropriate (e.g., `empty?`, `update!`).

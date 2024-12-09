# Rust Coding Standards

### General Best Practices
- Follow the [Rust API Guidelines](https://doc.rust-lang.org/nightly/style-guide/).
- Use descriptive function, variable, and type names to improve code readability.
- Leverage Rust's ownership model effectively, ensuring proper use of borrowing and lifetimes.
Avoid unnecessary use of unsafe blocks unless required and well-documented.

### Code Formatting
- Use rustfmt to enforce consistent code formatting.
- Indent using 4 spaces (no tabs).
- Use snake_case for variable, function, and module names.
- Use PascalCase for struct, enum, and trait names.
- Limit lines to 100 characters where possible.

### Testing
- Write unit tests using Rust's built-in testing framework with #[test].
- Group related tests within mod tests blocks.
- Use assert!, assert_eq!, and assert_ne! for test assertions.
- For expected failures, use the #[should_panic] attribute with a specific panic message.
- Ensure to follow the respective library's README file to verify correct testing commands and functionality.

### Additional Guidelines
- Prefer using Result and Option types for error handling instead of panicking.
- Use unwrap() and expect() sparingly, only in scenarios where failure is not expected.
- Document all public items (functions, structs, modules, etc.) using /// doc comments.
- Organize code logically with modules to keep the codebase clean and maintainable.
- When applicable, prefer iterator methods over manual loops for more idiomatic Rust code.
- Use clippy to lint code and catch common issues or anti-patterns.

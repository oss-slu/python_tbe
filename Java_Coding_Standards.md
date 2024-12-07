# Java Coding Standards

### General Best Practices
- Adhere to the [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html).
- Include Javadoc comments for all public classes and methods.
- Ensure methods are focused on a single task to improve testability.
- Soft limit of 100 characters per line.

### Code Formatting
- Use 4 spaces for indentation (no tabs).
- Use camelCase for variables and methods, and PascalCase for classes.
- Always use braces `{}` for control structures, even if optional.

### Testing
- Write unit tests for all methods using JUnit.
- Use `@Before` and `@After` annotations to set up and clean up test environments.
- Mock external dependencies where applicable.

### Additional Guidelines
- Avoid `System.out.println` for logging; use a logging framework like Log4j or SLF4J.

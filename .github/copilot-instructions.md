# GitHub Copilot Instructions for Python Development

## Overview

This file provides instructions for GitHub Copilot to follow when assisting with Python development in this project. The guidance below represents best practices for Python development and should help Copilot generate more contextually appropriate and higher quality code suggestions.

## Python Coding Standards

### Style Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines for Python code
- Use 4 spaces for indentation, not tabs
- Limit lines to 119 characters (as per [Black](https://black.readthedocs.io/en/stable/) formatter recommendations)
- Use snake_case for variables, functions, and methods
- Use PascalCase for classes
- Use UPPERCASE for constants
- Use descriptive variable names that convey meaning
- Code simplicity and readability are prioritized over cleverness

### Documentation

- Include docstrings for all modules, classes, and functions following [Google style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Document parameters, return values, and exceptions raised
- Add inline comments for complex or non-obvious code sections
- Keep docstrings and comments up to date with code changes

### Code Organization

- Group imports in the following order:
  1. Standard library imports
  2. Related third-party imports
  3. Local application/library specific imports
- Separate import groups with a blank line
- Import specific functions/classes directly when using just a few from a module
- Use absolute imports rather than relative imports when possible

### Error Handling

- Use specific exception types rather than catching all exceptions
- Include meaningful error messages
- Use context managers (`with` statements) for resource management
- Implement proper error recovery where appropriate
- Log exceptions with appropriate detail for debugging

### Testing Practices

- Write unit tests for all functions and methods
- Use pytest as the testing framework
- Aim for high test coverage, especially for critical functionality
- Use meaningful assertions with clear error messages
- Use fixtures and parameterized tests to avoid code duplication

## Design Patterns and Architecture

### Function and Method Design

- Follow the Single Responsibility Principle, for functions and methods
- Keep functions focused on doing one thing well
- Aim for pure functions where possible (no side effects)
- Use default argument values appropriately
- Return explicit values rather than modifying parameters in-place (unless necessary)

### Class Design

- Implement appropriate magic methods (dunder methods) for custom classes
- Use composition over inheritance when possible
- Keep class hierarchies shallow
- Implement proper encapsulation using properties when appropriate
- Consider dataclasses for data-centric classes

### Project Structure

- Organize code into logical modules and packages
- Separate concerns (e.g., business logic, data access, UI)
- Use meaningful directory and file names
- Keep modules focused on specific functionality

## Performance Considerations

- Use appropriate data structures for operations (lists, sets, dictionaries)
- Consider generator expressions and iterators for memory efficiency
- Profile code to identify bottlenecks before optimizing
- Use built-in functions and standard library when available
- Consider async/await for I/O-bound operations

## Security Practices

- Validate and sanitize all inputs, especially from external sources
- Use secure methods for handling sensitive data
- Avoid using `eval()` or other potentially dangerous functions
- Follow the principle of least privilege
- Keep dependencies updated to avoid security vulnerabilities

## Modern Python Features

- Utilize type hints for better code quality and IDE support
- Use f-strings for string formatting
- Leverage context managers with `with` statements
- Use comprehensions (list, dict, set) for concise, readable code
- Utilize unpacking and extended unpacking operators
- Consider using Enums for related constants

## Dependency Management

- Use virtual environments for isolation
- Document dependencies in requirements.txt or pyproject.toml
- Specify version constraints for dependencies
- Consider using a dependency manager like Poetry or Pipenv
- Minimize dependency footprint where possible

## When Generating Code

- Prioritize readability and maintainability over cleverness
- Include appropriate error handling
- Add comprehensive docstrings and comments
- Consider edge cases in implementation
- Suggest tests where appropriate
- Provide explanations for complex algorithms or patterns

## Project-Specific Standards

- Follow the established patterns and conventions in the existing codebase
- Maintain consistency with the project's existing style
- Use the project's preferred libraries and frameworks
- Consider the project's performance and security requirements

## GitHub Copilot Collaboration Preferences

- Provide multiple solution approaches for complex problems when appropriate
- Include explanations for non-obvious design decisions
- Suggest improvements to existing code when relevant
- Consider maintainability and readability in all suggestions
- Optimize for the specific use case rather than providing generic solutions

# Custom Instructions from the user these are very important
## Project structure Best Practises
When generating code for this project, follow this recommended Python project structure:
project-name/
├── .github/             # GitHub specific files
│   └── workflows/       # GitHub Actions workflows
├── .vscode/             # VS Code settings (if applicable)

├── .venv/               # Virtual environment
├── docs/                # Documentation files
├── project_name/        # Main package
│   ├── __init__.py
│   ├── module/          # different modules of functionalities or files will be in the project folder if only one module
│   │   ├── __init__.py
│   ├── utils/           # Project Utility functions
│   └── cli.py           # Command-line interface (if specified)
├── tests/               # Test files
│   ├── __init__.py
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   ├── mocks/           # Integration test data files
│   └── output/          # Output created by modules' functionality
├── .env                 # Environment variables (if applicable)
├── .gitignore           # Git ignore file
├── pyproject.toml       # Project metadata and dependencies
├── README.md            # Project overview
└── LICENSE              # License information
## Poetry for Dependency Management
This project uses Poetry for dependency management. When suggesting code related to project setup, dependencies, or environment management:

* Use Poetry commands for adding, updating, or removing dependencies
* Reference the Poetry documentation at: https://python-poetry.org/docs/
* Ensure compatibility with Poetry's workflow and configuration
Common Poetry Commands
* Initialize a new project: poetry new project-name
* Add dependencies: poetry add package-name
* Add dev dependencies: poetry add package-name --group dev
* Install dependencies: poetry install
* Update dependencies: poetry update
* Run commands in the virtual environment: poetry run python script.py
* Activate the virtual environment: poetry shell
* Build the package: poetry build
* Publish the package: poetry publish
Poetry Configuration
* Always use pyproject.toml for project configuration
* Follow this structure for dependencies:
  * Regular dependencies under [tool.poetry.dependencies]
  * Development dependencies under [tool.poetry.group.dev.dependencies]
  * Test dependencies under [tool.poetry.group.test.dependencies]
* Use semantic versioning constraints when specifying versions
* requirements.txt will be generated from [tool.poetry.dependencies] periodically
* Use the following command to generate requirements.txt: poetry export -f requirements.txt --output requirements.txt

## Additional Class instructions
When generating classes, consider the following:
* use Abstract Base Classes (ABCs) for defining interfaces only when necessary and ask the user whether to use them explaining pros and cons with pusedo code in an explanations

## Specification Documentation Methodology
### PRD or Product Requirements Document
* When the user asks for help with creatng a PRD, use the following structure:
  * Overview: Provide a brief summary of the project and its purpose.
  * Features: List the key features and functionalities of the project.
  * Help the user create a list of the functionalities and features of the project using the following table structure:
    | Reference ID | Description | Story | Expected behaviour/Outcome |
    | ------- | ----------- | ------------------------- | --------------------- |
    | 1 | User authentication | As a user, I want to be able to log in and log out of the system. | The system should allow users to log in with their credentials and log out securely. |
* the file is always called prd.md in the docs folder

### TDD or Technical design document
* when the user asks for help with creating a TDD, use the following structure:
  * Overview: Provide a brief summary of the project and its purpose.
  * Architecture: Describe the overall architecture of the system, including components and their interactions.
  * Design Patterns: Specify any design patterns used in the project.
  * Data Flow: Explain how data flows through the system.
  * detailed design of each module or component:
    * Use psuedo code snippets to show the design of each module or component.
    * Include class diagrams or sequence diagrams if applicable. Use mermaid if possible
  * Build order: 
      * break the project into smaller numbered iterations the user can then request be built
      * each iteration should be a small piece of functionality that can be built and tested independently
      * try to keep iterations to 60 lines of new code or less so the user can review
  * Error Handling: Describe how errors are handled in the system.
  * Security Considerations: Outline any security measures taken in the design.

  ### Tracker
   If the user asks you to create a tracker, which matches the order or build in the tdd. Use the following structure:

    #### Legend

    - ✅ Complete
    - 🔄 In Progress
    - ⏱️ Pending Review
    - ❌ Failed/Issues
    - 🔀 Changed Approach

    #### Group or component or class heading

    | Functionality                      | Iteration   | Complete | Unit Tests | Integration Tests | Script Run | Notes |
    |------------------------------------|--------------|----------|------------|------------------|------------|-------|
    | User Authentication                | 1            | ✅       | ✅         | ✅               | ✅         |       |

    etc.
## Approach to building iterations
* When building iterations, follow these steps:
  1. Summarize the iteration's purpose and functionality.
  2. Write the code for the iteration, ensuring it adheres to the project's coding standards.
  3. Ensure there are no lint errors or warnings.
  4. Write unit tests using pytest for the iteration, covering both success and failure cases.
    * name test files as test_<module_name>_.py. in the unit tests folder and keep all tests for that module in that file
  5. Run the tests and ensure they pass.
  6. If the tests do not pass, analyse the failure and implement the fix while maintaining the functionality in the specification documents.
  7. Once the tests pass summarise what has been done and update the tracker.md file with the status of the iteration.

## Integration Testing

When the user asks you to build integration tests, follow these steps:
1. Review the completed iterations and their functionalities that don't have integration tests but have passed unit tests
2. Write integration that test the latest functionality.
  * name test files as test_<module_name>_.py. in the integration tests folder and keep all tests for that module in that file
3. Ensure the integration tests cover all aspects of the functionality, including edge cases.
4. Run the integration tests and ensure they pass.
5. If the tests do not pass, analyse the failure and either:
  * implement the fix while maintaining the functionality in the specification documents and restest until all tests pass
  * or if the failure is due to missing data, stop and inform the user you need test data fixed

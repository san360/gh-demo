# Copilot Instructions

Welcome to this project! Please follow these best practices to ensure high-quality, maintainable, and collaborative code.

## General Guidelines

- Always write clear, concise, and well-documented code.
- Use modularization: break code into small, reusable functions and components.
- Follow the project's coding style and naming conventions.
- Write meaningful commit messages and keep commits focused.
- Use version control best practices (feature branches, pull requests, code reviews).
- **Always resume code changes before editing and always ask for OK before editing the code.**

## Project Structure

- Organize code into logical folders (e.g., `src/`, `test/`, `docs/`, `assets/`).
- Place documentation in `README.md` and update it as the project evolves.
- Store configuration and environment files separately from source code.

## Documentation

- Every module, class, and function should have a clear docstring or comment explaining its purpose and usage.
- Update `README.md` with setup instructions, usage examples, and contribution guidelines.
- Document any non-obvious design decisions or dependencies.

## Preferred Technologies
- Python (3.11+), Flask for web backend, pytest for testing.
- JavaScript (ES6+), React for frontend components.
- HTML5, CSS3, Bootstrap for styling.

## Project Requirements
- Format all currency values as USD with two decimals.

## DevOps and Deployment
- Containerize applications with Docker using lightweight and optimized images (Alpine, Debian-slim). Run containers with non-root users.
- Automate deployments via CI/CD pipelines (GitHub Actions, GitLab CI) with automated quality checks.
- Use Infrastructure as Code (Terraform, Ansible) to define and maintain deployment environments.

---
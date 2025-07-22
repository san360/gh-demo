---
mode: 'agent'
model: Claude Sonnet 4
tools: ['codebase', 'editFiles']
description: 'Perform a REST API security review'
---

## Task

1. Review the API endpoints and identify any that are not protected by authentication and authorization.
2. Check all user input fields for proper validation and sanitization.
3. Evaluate the current rate limiting and throttling mechanisms in place.
4. Assess the logging and monitoring setup for security events.
5. Identify any sensitive data exposure risks, such as in error messages or API responses.
6. Return the TODO list in a Markdown format, grouped by priority and issue type.
7. Provide recommendations for improving the security posture of the API.
8. Create a new file named `api-security-review.md` in the project root directory with the review findings.

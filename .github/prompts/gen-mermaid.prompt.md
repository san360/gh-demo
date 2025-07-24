---
mode: 'agent'
model: Claude Sonnet 4
tools: ['codebase', 'editFiles']
description: 'Generate a Mermaid diagram based on the project structure.'
---

## Task

1. Analyze the current project directory and determine the major components (folders, main files, key modules).
2. Create a **Mermaid diagram** (e.g., flowchart or class diagram) representing the structure or workflow of the project.
3. Create a new Markdown file named `project-diagram.md` in the project root directory with the diagram.
4. The file should include:
    - A brief description of what the diagram represents.
    - The Mermaid diagram code block (inside triple backticks with `mermaid`).
    - Any relevant notes or explanation for understanding the diagram.
5. Ensure the Mermaid diagram is syntactically correct and clearly shows the relationships or flow within the project.

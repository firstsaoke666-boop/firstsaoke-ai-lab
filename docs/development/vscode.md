# VS Code

Open the repository root in VS Code and install the workspace recommendations.
Select the Python environment created by `uv sync`; no interpreter path is
stored in repository settings.

The shared configuration formats Python with Ruff on save, applies Ruff fixes,
organizes imports, enables pytest, and hides generated files from search and
file watching. Use **Terminal > Run Task** for the standard `uv` and Makefile
commands. Debug configurations support the current Python file and the current
pytest file.

# Firstsaoke AI Workspace

## User Profile

- The user is a beginner.
- Give one small, verifiable step at a time.
- Clearly state where each action must be performed:
  - WSL Terminal
  - VS Code
  - Codex
  - Windows PowerShell
- Do not assume familiarity with Linux, Git, terminals, or project structure.

## Working Method

- Before changing files, briefly explain what will be changed.
- Only modify files directly related to the current task.
- Prefer small changes over large refactors.
- After each change, run the smallest relevant check.
- Stop after one meaningful step and wait for the user’s result.

## Context Control

- Do not recursively inspect the whole workspace unless explicitly requested.
- First inspect the top-level directory.
- Then read only the files required for the current task.
- Do not repeatedly reread unchanged files.
- Summarize large files instead of loading their entire contents when possible.

Do not inspect these directories unless explicitly requested:

- `.venv/`
- `venv/`
- `.git/`
- `node_modules/`
- `__pycache__/`
- `.pytest_cache/`
- `.mypy_cache/`
- `.ruff_cache/`
- `dist/`
- `build/`
- `.cache/`

## Security

- Never display or expose API keys, tokens, passwords, SSH keys, or `.env` contents.
- Do not modify authentication settings without explaining the change.
- Do not install dependencies without explaining why they are needed.
- Ask before deleting, moving, or overwriting files.

## Git Safety

Do not run these commands unless the user explicitly requests them:

- `git reset --hard`
- `git clean -fd`
- force push
- destructive history rewriting

Do not commit or push automatically.

## Code Quality

- Prefer readable code and descriptive names.
- Keep functions small and focused.
- Preserve existing behavior unless the task requires changing it.
- Avoid unrelated cleanup or unnecessary restructuring.
- Report which files changed and what verification was performed.
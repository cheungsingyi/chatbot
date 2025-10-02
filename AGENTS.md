# Agent Guidelines

## Commands
- **Build**: Check package.json for build scripts (typically `npm run build` or `python setup.py build`)
- **Lint**: Run `npm run lint` or `python -m flake8` or `ruff check`
- **Test**: Run `npm test` or `python -m pytest`
- **Single test**: `npm test -- <test-file>` or `python -m pytest <test-file>::<test-function>`

## Code Style
- **Imports**: Group imports (stdlib, third-party, local) with blank lines between groups
- **Formatting**: Use consistent indentation (4 spaces for Python, 2 for JS/TS)
- **Types**: Use type hints in Python, TypeScript interfaces/types
- **Naming**: snake_case for Python functions/variables, camelCase for JS/TS
- **Error handling**: Use try/catch in JS/TS, try/except in Python with specific exceptions
- **Comments**: Only when code is complex; prefer self-documenting code
- **Functions**: Keep under 50 lines, single responsibility
- **Classes**: Use PascalCase, keep methods focused

## Security
- Never log or expose secrets/keys
- Validate user inputs
- Use parameterized queries for database operations

## Git
- Commit logical units of work
- Use descriptive commit messages
- Never commit secrets or sensitive data
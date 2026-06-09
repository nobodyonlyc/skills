# Changelog Format

A changelog should be aimed at humans, not machines. Do not just blindly dump `git log` output into the file. Read the commit messages and categorize them logically.

## Aggregation Rules
Group the commits into the following sections in this exact order:

1. **⚠️ BREAKING CHANGES** (Any commit with a breaking change footer)
2. **✨ Features** (`feat:`)
3. **🐛 Bug Fixes** (`fix:`)
4. **🚀 Performance Improvements** (`perf:`)
5. **🛠️ Under the Hood** (`refactor:`, `chore:`, `build:`)
6. **📚 Documentation** (`docs:`)

## Formatting Rules
- Strip the conventional commit prefix (`feat:`, `fix:`) from the bullet points since the category header already provides that context.
- Keep the description concise.
- Include PR numbers or Issue numbers if present in the commit message (e.g., `(#142)`).
- Provide a brief summary paragraph at the top of the release notes if the release is significant (Major or Minor).

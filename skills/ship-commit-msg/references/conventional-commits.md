# Conventional Commits Specification

The commit message should be structured as follows:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

## 1. Type
Must be one of the following:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries such as documentation generation

## 2. Scope
The scope is an optional noun that provides contextual information (e.g., `feat(parser): add support for JSON`). It should be short and specific to the module/feature modified.

## 3. Description
- Must be 72 characters or less.
- Must be written in the **imperative, present tense**: "change" not "changed" nor "changes".
- Must not end with a period.
- Start with a lowercase letter.

## 4. Body
- Optional.
- Just like the description, use the imperative, present tense.
- Wrap lines at 72 characters.
- Use it to explain **what** and **why** vs. **how** (the code explains how).

## 5. Footer / Breaking Changes
- Optional.
- Any breaking changes **must** be highlighted in the footer with `BREAKING CHANGE: <description>`.
- Alternatively, you can use `!` after the type/scope (e.g., `feat(api)!: remove v1 endpoints`).
- References to issues should be in the footer (e.g., `Resolves #123`).

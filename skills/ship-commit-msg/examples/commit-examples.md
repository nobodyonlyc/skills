# Commit Message Examples

## Example 1: Standard Feature
```
feat(auth): implement JWT-based authentication

- Add token generation on login
- Implement middleware to verify tokens on protected routes
- Extract secret key to environment variables

Resolves #42
```

## Example 2: Bug Fix with Scope
```
fix(parser): handle null values gracefully in JSON payload

Previously, the parser would crash with a TypeError if the incoming JSON 
contained a null value for nested objects. We now default to an empty 
object in these cases to prevent the crash.
```

## Example 3: Breaking Change (Using `!`)
```
refactor(api)!: rename user endpoints for REST compliance

All endpoints starting with `/api/v1/getUsers` have been renamed to 
`/api/v1/users`.

BREAKING CHANGE: Client applications must update their API requests to 
use the new `users` resource path.
```

## Example 4: Chore (Dependency Update)
```
chore(deps): bump express from 4.17.1 to 4.18.2
```

## Example 5: Documentation
```
docs(readme): add setup instructions for local development
```

# Release Notes Example

Below is an example of what the generated output for `CHANGELOG.md` should look like.

```markdown
## [1.4.0] - 2024-06-09

This minor release introduces the new dark mode theme engine and resolves several long-standing issues with the authentication flow.

### ⚠️ BREAKING CHANGES
- **api**: The legacy `/api/v1/users` endpoint has been completely removed. Clients must migrate to `/api/v2/users`.

### ✨ Features
- **theme**: Implement system-aware dark mode (#214)
- **auth**: Add support for OAuth2 login via GitHub (#210)
- **ui**: Add new skeleton loaders for the dashboard grid

### 🐛 Bug Fixes
- **auth**: Prevent session timeout loops when token expires during a request (#218)
- **parser**: Handle null values gracefully in JSON payload (#205)

### 🚀 Performance Improvements
- **db**: Add compound indexes for user queries, speeding up dashboard load by 40%

### 🛠️ Under the Hood
- **deps**: Bump express from 4.17.1 to 4.18.2
- **core**: Refactor the event emitter to use native Promises
```

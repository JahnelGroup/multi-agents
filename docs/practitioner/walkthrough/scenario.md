# Add user authentication middleware

## Issue

Add user authentication middleware to the Node.js/Express application. Implement a login endpoint that issues JWT tokens and middleware that validates tokens on protected routes.

## Acceptance Criteria

1. **POST /auth/login** accepts email and password, returns a JWT token on success.
2. **Middleware** validates JWT on protected routes and returns 401 if the token is invalid or expired.
3. **Tests** cover valid token, expired token, and missing token scenarios.

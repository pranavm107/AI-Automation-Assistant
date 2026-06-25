# Authentication Guide

## Overview
The AI Career Intelligence Platform uses JWT (JSON Web Tokens) for stateless, secure authentication.

## Token Lifecycle
1. **Login**: User provides email and password. Server returns `access_token` (15 min) and `refresh_token` (7 days).
2. **Accessing APIs**: Client places the `access_token` in the `Authorization` header as a Bearer token.
3. **Expiration**: When the `access_token` expires, the client uses the `refresh_token` to request a new `access_token` without requiring the user to log in again.
4. **Logout**: Client deletes tokens from local storage, and the server revokes the `refresh_token` to prevent future sessions.

## Role-Based Access Control
- **USER**: Standard role assigned on registration. Can upload and query their own documents.
- **PREMIUM**: Future role for advanced LLM functionality limits.
- **ADMIN**: Can view global platform statistics.

## Frontend Context
The React Frontend utilizes `AuthContext` to globally distribute the `user` object and intercept Axios calls to inject tokens. `ProtectedRoute` prevents unauthorized users from accessing the `/dashboard` or any tool workflows.

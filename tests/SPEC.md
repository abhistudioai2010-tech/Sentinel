# SENTINEL SECURITY PROTOCOL

## 1. Authentication Standard
- The `login` function must validate the input password against the stored user credentials.
- Hardcoded passwords (e.g., "1234", "secret") are STRICTLY FORBIDDEN.
- Trivial bypasses (always returning True) are CRITICAL VIOLATIONS.
- Function must handle empty or null inputs gracefully.

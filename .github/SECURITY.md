# Security Policy

## Supported Versions

We actively support the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please follow these steps:

### 1. **Do NOT** create a public GitHub issue
Security vulnerabilities should not be disclosed publicly until they have been addressed.

### 2. Report privately
Send an email to: **elwaycortez@gmail.com**

Include the following information:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Any suggested fixes (if available)

### 3. Response Timeline
- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Depends on severity (1-30 days)

### 4. Disclosure Process
1. We will acknowledge receipt of your report
2. We will investigate and validate the vulnerability
3. We will develop and test a fix
4. We will release a security update
5. We will publicly disclose the vulnerability (with credit to reporter, if desired)

## Security Best Practices

### For Users
- Always use the latest version from PyPI: `pip install --upgrade tilapia-freshness-evaluator`
- Verify package integrity: Check PyPI checksums
- Use virtual environments to isolate dependencies
- Keep your Python environment updated

### For Contributors
- Follow secure coding practices
- Never commit secrets, API keys, or credentials
- Use dependency scanning tools
- Report security issues through proper channels

## Dependencies Security

We regularly monitor our dependencies for security vulnerabilities:
- **OpenCV**: Updated to latest secure version
- **Pillow**: Updated to latest secure version  
- **NumPy**: Updated to latest secure version

## Contact

For security-related questions or concerns:
- **Email**: elwaycortez@gmail.com
- **GitHub**: [@Evrouin](https://github.com/Evrouin)

Thank you for helping keep our project secure! 🔒

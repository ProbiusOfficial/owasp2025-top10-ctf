<p align="right">
  <strong>English</strong> | <a href="./README.zh-CN.md">简体中文</a>
</p>

# OWASP Top 10:2025 CTF Challenge Collection

<p align="center">
  <img src="https://img.shields.io/badge/OWASP-Top%2010%202025-red?style=for-the-badge&logo=owasp&logoColor=white" alt="OWASP Top 10 2025">
  <img src="https://img.shields.io/badge/CTF-24%20Challenges-blue?style=for-the-badge" alt="24 Challenges">
  <img src="https://img.shields.io/badge/Docker-Supported-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Supported">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License MIT">
</p>

> A collection of **24 CTF challenges** (8 categories × 3 difficulty levels) based on the **OWASP Top 10:2025** framework. Each challenge is deployed as a single container with dynamic flag injection support, suitable for CTF competitions, security training, and penetration testing education.

---

## Challenge Overview

| OWASP Category | Count | Easy | Medium | Hard |
|---------------|-------|------|--------|------|
| **A01** Broken Access Control | 3 | IDOR Horizontal Bypass | JWT Frontend Bypass | SSRF + IP Encoding Bypass |
| **A02** Security Misconfiguration | 3 | `.git` Directory Leak | Missing Security Headers + XSS Bypass | XXE External Entity Injection |
| **A04** Cryptographic Failures | 3 | Weak Random Token Prediction | CBC Bit-Flipping Attack | JWT Algorithm Confusion RS256→HS256 |
| **A05** Injection | 3 | SQL Injection | SSTI (Jinja2) | Command Injection + Blacklist Bypass |
| **A06** Insecure Design | 3 | Payment Logic Bypass | Race Condition | Batch Operation Unauthorized Access |
| **A07** Authentication Failures | 3 | Weak Password Brute Force | JWT Weak Key Brute Force | Password Reset Token Prediction |
| **A08** Data Integrity Failures | 3 | Prototype Pollution (lodash) | Pickle Deserialization RCE | PHP Deserialization POP Chain |
| **A10** Exception Handling | 3 | Error Information Disclosure | Fail Open | Exception-Based Side-Channel Blind Injection |

**Total: 8 Categories × 3 Levels = 24 Challenges**

---

## Quick Start

### Directory Structure

```
CTF-Challenges/
├── A01-BrokenAccessControl/
│   ├── easy/          # IDOR Horizontal Privilege Bypass
│   ├── medium/        # JWT Frontend Privilege Bypass
│   └── hard/          # SSRF + IP Encoding Bypass
├── A02-SecurityMisconfiguration/
│   ├── easy/          # .git Directory Leak
│   ├── medium/        # Missing Security Headers + XSS Bypass
│   └── hard/          # XXE External Entity Injection
├── A04-CryptographicFailures/
│   ├── easy/          # Weak Random Token Prediction
│   ├── medium/        # CBC Bit-Flipping Attack
│   └── hard/          # JWT Algorithm Confusion Attack
├── A05-Injection/
│   ├── easy/          # SQL Injection
│   ├── medium/        # SSTI (Jinja2)
│   └── hard/          # Command Injection + Blacklist Bypass
├── A06-InsecureDesign/
│   ├── easy/          # Payment Logic Bypass
│   ├── medium/        # Race Condition
│   └── hard/          # Batch Operation Unauthorized Access
├── A07-AuthenticationFailures/
│   ├── easy/          # Weak Password Brute Force
│   ├── medium/        # JWT Weak Key Brute Force
│   └── hard/          # Password Reset Token Prediction
├── A08-DataIntegrityFailures/
│   ├── easy/          # Prototype Pollution (Node.js)
│   ├── medium/        # Pickle Deserialization RCE
│   └── hard/          # PHP Deserialization POP Chain
└── A10-ExceptionHandling/
    ├── easy/          # Error Information Disclosure
    ├── medium/        # Fail Open
    └── hard/          # Exception-Based Side-Channel Blind Injection
```

### Standard Files per Challenge

```
<difficulty>/
├── src/               # Application source code
│   ├── app.py         # Main application (or app.js / index.php)
│   ├── requirements.txt / package.json
│   └── ...            # Other source files
├── Dockerfile         # Single container build
├── docker-compose.yml # For local testing only
├── README.md          # Challenge description
└── WriteUP.md         # Full write-up and solution
```

---

## Dynamic Flag Injection

All challenges support dynamic flag injection via environment variables:

| Variable | Description |
|---------|-------------|
| `DASFLAG` | Primary flag variable |
| `FLAG` | Fallback flag variable |
| `GZCTF_FLAG` | GZCTF platform flag variable |

The flag is automatically written to `/flag` inside the container during startup for the application to read.

### Local Testing

```bash
cd <challenge-directory>
docker-compose up -d
# Access http://localhost:<port>
```

---

## Challenge Details

### A01 - Broken Access Control

| Difficulty | Challenge Name | Vulnerability Type | Key Technique |
|------------|---------------|-------------------|---------------|
| Easy | Document Viewer | IDOR | Modify URL parameter `doc_id` to access unauthorized documents |
| Medium | Privilege Management | JWT Frontend Bypass | Frontend hides admin features; backend API does not validate roles |
| Hard | Image Fetch Service | SSRF | Bypass blacklist via decimal/hexadecimal/octal IP encoding to access internal network |

### A02 - Security Misconfiguration

| Difficulty | Challenge Name | Vulnerability Type | Key Technique |
|------------|---------------|-------------------|---------------|
| Easy | Company Website | .git Leak | Retrieve sensitive files from `.git` directory history |
| Medium | Message Board | XSS Bypass | Double encoding bypasses string replacement filter; missing CSP |
| Hard | XML Processor | XXE | Exploit external entities to read `/flag`; UTF-16 encoding bypass |

### A04 - Cryptographic Failures

| Difficulty | Challenge Name | Vulnerability Type | Key Technique |
|------------|---------------|-------------------|---------------|
| Easy | Token Generator | Weak Randomness | Predict pseudo-random seed based on timestamp |
| Medium | Cookie Encryption | CBC Bit-Flipping | Flip plaintext `role` field by modifying ciphertext block |
| Hard | JWT Authentication | Algorithm Confusion | Forge signature using RS256 public key as HS256 HMAC key |

### A05 - Injection

| Difficulty | Challenge Name | Vulnerability Type | Key Technique |
|------------|---------------|-------------------|---------------|
| Easy | User Query System | SQL Injection | Classic string-concatenation SQLi with `UNION SELECT` to read flag |
| Medium | Email Template Generator | SSTI | Jinja2 template injection using `\|attr()` + list concatenation to bypass filters |
| Hard | Ping Test Tool | Command Injection | Blacklist filter bypass using newlines + input redirection |

### A06 - Insecure Design

| Difficulty | Challenge Name | Vulnerability Type | Key Technique |
|------------|---------------|-------------------|---------------|
| Easy | Gold Coin Shop | Payment Logic Bypass | Frontend calculates amount; backend trusts frontend-supplied parameters |
| Medium | Flash Sale | Race Condition | TOCTOU vulnerability; concurrent requests lead to overselling |
| Hard | Notes App | Batch Unauthorized Access | Batch query only validates the first ID; subsequent IDs are unchecked |

### A07 - Authentication Failures

| Difficulty | Challenge Name | Vulnerability Type | Key Technique |
|------------|---------------|-------------------|---------------|
| Easy | Login System | Weak Password | Unprotected brute force with common weak password dictionary |
| Medium | JWT Authentication | Weak Key | Brute force HS256 key with dictionary to forge admin token |
| Hard | Password Reset | Token Prediction | Predictable `MD5(user_id:timestamp)`; brute force within time window |

### A08 - Data Integrity Failures

| Difficulty | Challenge Name | Vulnerability Type | Key Technique |
|------------|---------------|-------------------|---------------|
| Easy | Config Update Service | Prototype Pollution | `_.merge()` does not filter `__proto__`, polluting `isAdmin` |
| Medium | Data Serialization Service | Pickle RCE | `pickle.loads()` directly deserializes user input, leading to command execution |
| Hard | Object Deserialization | PHP POP Chain | `unserialize()` triggers `__destruct`→`__toString` chain to read files |

### A10 - Exception Handling

| Difficulty | Challenge Name | Vulnerability Type | Key Technique |
|------------|---------------|-------------------|---------------|
| Easy | File Viewer | Information Disclosure | Exceptions return full stack traces, leaking SECRET_KEY |
| Medium | Admin Panel | Fail Open | `except Exception: return True` causes authentication bypass |
| Hard | Password Verification | Side-Channel | Exception messages leak matched prefix length, enabling byte-by-byte blind injection |

---

## Tech Stack Distribution

| Stack | Challenge Count |
|-------|----------------|
| Python Flask | 21 |
| Node.js + Express | 1 (A08-easy) |
| PHP + Nginx | 1 (A08-hard) |

---

## Usage Guide

### For Players
1. Read the `README.md` in each challenge directory to understand the scenario
2. Try to solve the challenge independently
3. Refer to `WriteUP.md` when stuck

### For Organizers / Platform Operators
1. Each challenge directory contains a complete `Dockerfile` for direct image building
2. Use `docker-compose.yml` for local testing
3. Inject dynamic flags via environment variables during deployment
4. All challenges are **single-container** designs, compatible with most CTF platforms (docker-compose is for local testing only)

---

## References

The challenges in this project are designed based on the following authoritative resources:

- **[OWASP Top 10:2025](https://owasp.org/Top10/2025/)** — The official OWASP Foundation list of the top 10 Web security risks for 2025

> ⚠️ **Note**: The OWASP numbering (e.g., A01, A02) in this project strictly follows the official OWASP Top 10:2025 classification. Some categories from the 2021 edition have been merged or adjusted in the 2025 edition.

---

## Generative AI Usage Disclosure

Parts of the documentation in this project (including but not limited to the root `README.md`, challenge description optimization, and write-up organization) were assisted by generative AI tools (such as Kimi, GPT series, etc.):

- **AI Assistance Scope**: Document structure optimization, language polishing, formatting standardization, and translation assistance.
- **Human Review**: All security-related technical content, vulnerability designs, and source code implementations are manually written and reviewed to ensure technical accuracy.
- **Disclaimer**: AI-generated content is for reference only; actual vulnerability exploitation and remediation should be verified in specific environments.

If you find any inaccuracies resulting from AI assistance, please feel free to submit an Issue or Pull Request for correction.

---

## License

This project is open-sourced under the [MIT License](LICENSE).

```text
MIT License

Copyright (c) 2026 ProbiusOfficial

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

> ⚠️ Although the code is open-sourced under the MIT License, the vulnerabilities in the challenges are **intentionally designed** for educational purposes only. Do not use the related techniques on unauthorized systems.

---

## Disclaimer

This challenge collection is intended solely for security learning, CTF competitions, and penetration testing training. All vulnerabilities are deliberately designed. Please do not use them for illegal purposes.

When using this project, please ensure:
- Run challenge containers only in authorized environments
- Comply with local laws and regulations
- Do not use the techniques involved on any third-party systems without authorization

---

<p align="center">
  Based on the official <a href="https://owasp.org/Top10/2025/">OWASP Top 10:2025</a><br>
  Made with ❤️ for the CTF & Security Community
</p>

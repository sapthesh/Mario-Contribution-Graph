# 🛡️ Security Policy

## Supported Versions

We are committed to keeping the **Mario-GitHub-Contribution-Graph** secure. Because this project interacts with GitHub's GraphQL API and uses automation tokens, security is a top priority.

| Version | Supported          |
| ------- | ------------------ |
| latest  | ✅ Supported       |
| < 1.0.0 | ❌ Not Supported   |

---

## Reporting a Vulnerability

If you discover a security vulnerability within this project, please **do not open a public issue**. Publicly disclosing a vulnerability can put users at risk. Instead, please follow the steps below to report it privately.

### 📧 How to Report
Please create an issue with the following details:
* A description of the vulnerability.
* Steps to reproduce the issue.
* Any potential impact (e.g., token exposure, script injection).

### ⏳ Our Response
Once a report is received, you can expect the following timeline:

| Stage | Timeline |
|---|---|
| **Acknowledgment** | Within 48 hours of receipt. |
| **Investigation** | Detailed analysis within 5 business days. |
| **Fix/Patch** | Priority based on severity (Critical issues patched ASAP). |

---

## Security Best Practices for Users

Since this project requires a `GITHUB_TOKEN` to function, we strongly recommend the following:

| Recommendation | Reason |
|---|---|
| **Use Default Secrets** | Always use `${{ secrets.GITHUB_TOKEN }}` in your workflow. This is a short-lived, automatic token provided by GitHub. |
| **Minimize Scopes** | Ensure your workflow only has `contents: write` permissions. Do not grant unnecessary administrative access. |
| **Audit Logs** | Regularly check your GitHub Actions execution logs to ensure the script is behaving as expected. |

---

## Disclosure Policy

We follow a **Responsible Disclosure** policy. We ask that you give us a reasonable amount of time to fix the issue before making any information public. In return, we will provide full credit to the researcher who discovered the vulnerability (unless they wish to remain anonymous).

Thank you for helping keep the Mario graph safe for everyone!

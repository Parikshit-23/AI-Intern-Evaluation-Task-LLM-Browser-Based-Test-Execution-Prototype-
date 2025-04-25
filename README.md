# AI-Intern-Evaluation-Task-LLM-Browser-Based-Test-Execution-Prototype
# AI-Powered Browser Automation for Web Testing

This project demonstrates an AI-driven browser automation system built for an internship task using:

-  Large Language Model (LLM) for step parsing (Claude 3 Haiku via OpenRouter)
-  Real browser automation using Playwright
-  Intelligent step execution and validation
-  Self-healing logic

---

## Project Overview

The script takes a test case in natural language and automates the process of:

1. **Parsing natural steps** (e.g., "Click on the 'My account' link") into structured browser commands using an LLM.
2. **Executing those steps** in a real Chromium browser using Playwright.
3. **Validating the expected result** on the final page.
4. (Bonus planned) Implementing self-healing logic to retry failed steps or try fallbacks.

---

## Python libraries required
```bash
pip install openai
pip install playwright
pip install json
```

---


## Technologies Used

| Component | Purpose |
|----------|---------|
| **OpenRouter + Claude 3 Haiku** | Natural language understanding & JSON command generation |
| **Playwright (Python)** | Real browser automation and interaction |
| **Python 3.11+** | Required for compatibility with `playwright` and newer LLM clients |

---

## Prompt Design Strategy

### Goal:
> Convert a series of plain-English test steps into a structured array of browser actions.

### Example Prompt Sent to LLM:

```plaintext
You are an automation assistant. Convert these steps into a valid JSON array 
of browser commands. ONLY return valid JSON — do not explain anything.

Steps:
Click on the 'My account' link
Enter email as 'test@example.com'
Enter password as 'test123'
Click on the login button

Example Output:
[
  {"action": "click", "target": "a:has-text('My account')"},
  {"action": "type", "target": "input[type='email']", "value": "test@example.com"},
  {"action": "type", "target": "input[type='password']", "value": "test123"},
  {"action": "click", "target": "button:has-text('Sign in')"}
]

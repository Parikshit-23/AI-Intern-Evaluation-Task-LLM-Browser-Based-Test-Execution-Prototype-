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
```
```bash
pip install playwright
```
```bash
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
Prompt:
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

---

## Execution and Validation Logic

### Execution
**The script uses sync_playwright to:**

1. Open a Chromium browser

2. Navigate to the test URL (https://www.farmley.com)

3. Sequentially perform click and type actions on the page

4. Wait for page updates using page.wait_for_timeout()

### Validation
**After steps are executed:**

1. It checks the final page's HTML content

2. Compares it to the expected_output string

3. Returns either:

   PASS (if expected content found)

   FAIL (if not)

---

## Challenges and How They Were Solved
** Problem 1: LLM returned invalid or non-parsable JSON**
Solution:

Used Claude 3 Haiku, which is known to return clean JSON.

Stripped Markdown formatting (like ```json).

Added json.loads() error checks and print() for debugging.

** Problem 2: Unable to use Browser-Use to execute steps on live site**
Solution:

Used Playwright to perform that task on live site

---

## Bonus: Self-Healing Logic (Planned)
To make the automation more robust, these enhancements are planned:

Retry failed steps with alternate selectors

Log failing step index + take screenshots (e.g., step_3_fail.png)

Add try-except blocks to continue past non-critical failures


---


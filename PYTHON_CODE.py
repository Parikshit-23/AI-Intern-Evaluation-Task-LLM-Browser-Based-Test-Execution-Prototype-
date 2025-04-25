
import json
from openai import OpenAI
from playwright.sync_api import sync_playwright


# CONFIGURATION 
# OpenRouter LLM client setup
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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" 
)

# Example test input
test_input = {
    "url": "https://www.farmley.com/",
    "test_case": {
        "steps": [
            "Click on the 'My account' link",
            "Enter email as 'test@example.com'",
            "Enter password as 'test123'",
            "Click on the login button"
        ],
        "expected_output": "My Account"
    }
}


# LLM Parsing 

def ask_llm_to_parse_steps(steps):
    """Use LLM to convert natural steps into structured actions."""
    # Defining example output with steps to be performed
    example_output = """[
      {"action": "click", "target":"a:has-text('My account')"},
      {"action": "type", "target": "input[type='email']", "value": "test@example.com"},
      {"action": "type", "target": "input[type='password']", "value": "test123"},
      {"action": "click", "target": "button:has-text('Sign in')"}
    ]"""
    # This is the prompt which informs the LLM to generate response in valid json format step by step 
    prompt = (
    f"You are an automation assistant. Convert these steps into a valid JSON array "
    f"of browser commands. ONLY return valid JSON — do not explain anything.\n\n"
    f"Steps:\n{steps}\n\n"
    f"Example Output:\n{example_output}"
    )
    # LLM used is claude 3 haiku
    response = client.chat.completions.create(
        model="anthropic/claude-3-haiku",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    # This function returns the LLM's response in valid json format
    return json.loads(response.choices[0].message.content)


# Run Steps in Playwright
# Playwright is used in order to communicate with browser and to execute the steps on live site
# This function tests whether the task is completed successfully or not
def run_test(url, steps, expected_text):
    # Initializing the browser using playwright (Staarting the browser)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(url)
        
        for i, step in enumerate(steps, 1):
            action = step["action"]
            target = step["target"]
            value = step.get("value")
            
            # Using exception handling to check whether all steps are performed successfully
            # Target steps which are mentioned in 'example_output'
            try:
                print(f"-> Step {i}: {action} -> {target}")
                if action == "click":
                    try:
                        page.click(target, timeout=5000)
                    except:
                        # fallback: try a different way to click
                        print(f"Primary selector failed, trying locator fallback for: {target}")
                        page.locator(target).click(timeout=5000)
                elif action == "type":
                    page.fill(target, value)
            # Another fallback strategy is to capture screenshot of a particular step that has failed
            except Exception as e:
                print(e)
                print(f"Step {i} failed: {e}")
                page.screenshot(path=f"step_{i}_ss.png")
                continue  # It will not crash, instead it will move to next step

        page.wait_for_timeout(3000)
        content = page.content().lower()
        browser.close()
        
        return "PASS" if expected_text.lower() in content else "FAIL"
        # It will print a brief note of all steps and at last it will print PASS or FAIL




# MAIN EXECUTION

def main():
    url = test_input["url"]
    steps_natural = test_input["test_case"]["steps"]
    expected_output = test_input["test_case"]["expected_output"]

    print("[1] Asking LLM to parse test steps...",end='\n')
    structured_steps = ask_llm_to_parse_steps(steps_natural)
    print("Structured steps:", structured_steps,end='\n')

    print("\n[2] Running test through Playwright...",end='\n')
    result = run_test(url, structured_steps, expected_output)

    print("\n[3] Final Result : ", result,end='\n')
    

if __name__ == "__main__":
    main()

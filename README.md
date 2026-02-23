# LLM Unit Test Generator CLI

A deterministic Python command-line developer tool that generates strict, runnable unit tests for a single Python function using an LLM API.

This tool is designed to behave like a specialized developer utility — not a chatbot — by enforcing strict scope validation, output constraints, and security safeguards.

---

## Problem Context

Large legacy codebases often lack automated tests, making refactoring risky and slowing development cycles.

This tool automates unit test generation while enforcing:

- Strict scope validation
- Deterministic output behavior
- No markdown or explanations
- Protection against prompt injection
- Sanitized input handling

---

## Features

- ✅ Accepts source code containing a single Python function
- ✅ Validates that exactly one function is present
- ✅ Rejects out-of-scope queries
- ✅ Calls an LLM API to generate tests
- ✅ Enforces strict output constraints:
  - No markdown
  - No explanations
  - No commentary
  - Valid Python only
- ✅ Ensures required imports are present (e.g., `import pytest`)
- ✅ Deterministic behavior via controlled prompt and parameters
- ✅ Optional file output support
- ✅ Protects against prompt injection inside source code

---

## How to Run the Application

### 1) Clone the Repository

```bash
git clone https://github.com/passantelsherif/llm-unit-test-generator-cli.git
cd llm-unit-test-generator-cli/unit_test_gen_cli
```

### 2) Set Required Environment Variables

```bash
$env:LLM_ENDPOINT="https://openrouter.ai/api/v1/chat/completions"
$env:LLM_API_KEY="your_api_key_here"
$env:LLM_MODEL="arcee-ai/trinity-large-preview:free"
```

### 3) Generate Tests (Print to Terminal)
```bash
python .\main.py --file .\sample_input.py --framework pytest
```

### 4) Generate Tests and Save to a Separate File
using the --out argument:

```bash
python .\main.py --file .\sample_input.py --framework pytest --out .\generated_tests.py
```
### 5) Run the Generated Tests (Optional)
If using pytest:
```bash
pytest .\generated_tests.py
```

Make sure pytest is installed:
```bash
pip install pytest
```











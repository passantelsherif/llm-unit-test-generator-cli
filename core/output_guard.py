import ast
from core.errors import OutputConstraintError


def _reject_if_contains_markdown(text: str) -> None:
    if "```" in text:
        raise OutputConstraintError("Markdown detected")


def _reject_if_contains_explanations(text: str) -> None:
    lowered = text.lower()
    banned_phrases = [
        "here are", "below are", "explanation", "this test", "we will", "the function",
        "sure", "of course", "i will", "let's",
    ]
    if any(p in lowered for p in banned_phrases):
        raise OutputConstraintError("Explanation-like text detected")


def _must_look_like_tests(text: str, framework: str) -> None:
    if framework == "pytest":
        if "def test_" not in text:
            raise OutputConstraintError("No pytest-style test functions found")
    else:
        if "unittest" not in text and "TestCase" not in text:
            raise OutputConstraintError("No unittest-style structure found")


def _enforce_required_imports(text: str, framework: str) -> None:
    """
    If the output uses pytest (pytest.raises, pytest.mark, etc.),
    it must include an import for pytest.
    """
    if framework == "pytest":
        uses_pytest = ("pytest." in text) or ("@pytest." in text)
        has_pytest_import = ("import pytest" in text) or ("from pytest" in text)
        if uses_pytest and not has_pytest_import:
            raise OutputConstraintError("Uses pytest but missing 'import pytest'")


def _must_be_valid_python(text: str) -> None:
    try:
        ast.parse(text)
    except SyntaxError:
        raise OutputConstraintError("Output is not valid Python")


def enforce_tests_only(output: str, framework: str) -> str:
    cleaned = output.strip() + "\n"
    _reject_if_contains_markdown(cleaned)
    _reject_if_contains_explanations(cleaned)
    _must_look_like_tests(cleaned, framework)
    _enforce_required_imports(cleaned, framework)  
    _must_be_valid_python(cleaned)
    return cleaned

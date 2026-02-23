from core.errors import OutOfScopeError


def validate_non_empty(text: str) -> None:
    if not text or not text.strip():
        raise OutOfScopeError("Empty input")


def validate_looks_like_code(text: str) -> None:
    stripped = text.strip()
    if len(stripped) < 10:
        raise OutOfScopeError("Too short to be code")

    hints = ("def ", "class ", "import ", "from ", "return", ":", "(")
    if not any(h in stripped for h in hints):
        raise OutOfScopeError("Does not look like Python source code")

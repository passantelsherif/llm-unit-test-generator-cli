OUT_OF_SCOPE_MESSAGE = "Error: This tool only generates unit tests for functions."

class ToolError(Exception):
    """Base class for tool errors."""
 
class OutOfScopeError(ToolError):
    """Raised when the request is out of scope."""

class ValidationError(ToolError):
     """Raised for validation errors within scope (optional)."""

class ParseError(ToolError):
    """Raised when there is an error parsing the input."""

class SanitizationError(ToolError):
    """Raised when sanitization fails."""

class LLMError(ToolError):
    """Raised when the LLM API call fails."""

class OutputConstraintError(ToolError):
    """Raised when the output violates constraints."""

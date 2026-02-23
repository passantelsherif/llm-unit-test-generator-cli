import ast
import io
import tokenize
from core.errors import SanitizationError
from core.types import FunctionInfo


def strip_comments(code: str) -> str:
    out_tokens = []
    try:
        tokgen = tokenize.generate_tokens(io.StringIO(code).readline)
        for tok_type, tok_str, start, end, line in tokgen:
            if tok_type == tokenize.COMMENT:
                continue
            out_tokens.append((tok_type, tok_str))
        return tokenize.untokenize(out_tokens)
    except tokenize.TokenError as e:
        raise SanitizationError(f"Tokenize failed: {e}")


def strip_docstring_from_function(code: str) -> str:
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        raise SanitizationError("Cannot parse function segment")

    if not tree.body or not isinstance(tree.body[0], (ast.FunctionDef, ast.AsyncFunctionDef)):
        return code

    fn = tree.body[0]
    if fn.body and isinstance(fn.body[0], ast.Expr):
        value = fn.body[0].value
        is_doc = (isinstance(value, ast.Constant) and isinstance(value.value, str)) or isinstance(value, ast.Str)
        if is_doc:
            fn.body = fn.body[1:]

    if hasattr(ast, "unparse"):
        try:
            rebuilt = ast.unparse(tree)
            return rebuilt + "\n"
        except Exception:
            return code

    return code


def sanitize_function_source(func_info: FunctionInfo) -> str:
    without_comments = strip_comments(func_info.source_segment)
    without_docstring = strip_docstring_from_function(without_comments)
    return without_docstring.strip() + "\n"

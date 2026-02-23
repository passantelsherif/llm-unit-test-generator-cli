import ast
from typing import List, Tuple
from core.types import FunctionInfo
from core.errors import ParseError, OutOfScopeError


def _collect_top_level_functions(tree: ast.AST) -> List[ast.AST]:
    funcs: List[ast.AST] = []
    for node in getattr(tree, "body", []):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append(node)
    return funcs


def _get_arg_names(fn: ast.AST) -> List[str]:
    assert isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef))
    return [a.arg for a in fn.args.args]


def _extract_source_segment(text: str, fn: ast.AST) -> str:
    if not hasattr(fn, "lineno") or not hasattr(fn, "end_lineno"):
        raise ParseError("AST nodes missing line metadata")
    lines = text.splitlines(keepends=True)
    start = fn.lineno - 1
    end = fn.end_lineno  
    segment = "".join(lines[start:end])
    return segment


def extract_single_function(text: str) -> FunctionInfo:
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        raise OutOfScopeError("Invalid Python syntax")  

    funcs = _collect_top_level_functions(tree)

    if len(funcs) == 0:
        raise OutOfScopeError("No function found")

    if len(funcs) > 1:
        raise OutOfScopeError("Multiple functions found")

    fn = funcs[0]
    assert isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef))

    name = fn.name
    args = _get_arg_names(fn)
    segment = _extract_source_segment(text, fn)
    is_async = isinstance(fn, ast.AsyncFunctionDef)

    return FunctionInfo(name=name, args=args, source_segment=segment, is_async=is_async)

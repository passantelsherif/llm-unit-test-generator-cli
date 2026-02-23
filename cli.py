import argparse
import sys
from core.types import InputPayload
from core.errors import OutOfScopeError


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(add_help=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="Path to a file containing a single function.")
    group.add_argument("--stdin", action="store_true", help="Read source code from stdin.")
    parser.add_argument(
        "--framework",
        type=str,
        default="pytest",
        choices=["pytest", "unittest"],
        help="Test framework to generate.",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Write generated tests to this file instead of printing to stdout.",
    )
    return parser.parse_args(argv)


def read_input(opts: argparse.Namespace) -> InputPayload:
    if opts.file:
        try:
            with open(opts.file, "r", encoding="utf-8") as f:
                return InputPayload(raw_text=f.read(), source_hint=opts.file)
        except OSError as e:
            raise OutOfScopeError(str(e))

    if opts.stdin:
        text = sys.stdin.read()
        return InputPayload(raw_text=text, source_hint="stdin")

    raise OutOfScopeError("No input provided")

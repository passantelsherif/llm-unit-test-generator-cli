from pathlib import Path
from core.types import InputPayload, PipelineResult
from core.errors import OutOfScopeError, OUT_OF_SCOPE_MESSAGE, ToolError
from core import validator, parser, sanitizer, prompt_builder, llm_client, output_guard


def run_pipeline(payload: InputPayload, framework: str) -> PipelineResult:
    validator.validate_non_empty(payload.raw_text)
    validator.validate_looks_like_code(payload.raw_text)

    func_info = parser.extract_single_function(payload.raw_text)

    safe_code = sanitizer.sanitize_function_source(func_info)

    llm_req = prompt_builder.build_llm_request(safe_code, func_info, framework=framework)

    raw_output = llm_client.call_llm(llm_req)

    tests_only = output_guard.enforce_tests_only(raw_output, framework=framework)

    module_name = Path(payload.source_hint).stem

    import_line = f"from {module_name} import {func_info.name}\n\n"

    final_tests = import_line + tests_only

    return PipelineResult(tests_text=final_tests)


def render_error(e: Exception) -> str:
    if isinstance(e, OutOfScopeError):
        return OUT_OF_SCOPE_MESSAGE

    if isinstance(e, ToolError):
        return OUT_OF_SCOPE_MESSAGE

    return OUT_OF_SCOPE_MESSAGE

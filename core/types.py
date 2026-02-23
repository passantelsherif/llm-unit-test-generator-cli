from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class InputPayload:
    raw_text: str
    source_hint: str  


@dataclass(frozen=True)
class FunctionInfo:
    name: str
    args: List[str]
    source_segment: str
    is_async: bool


@dataclass(frozen=True)
class LLMRequest:
    system_prompt: str
    user_prompt: str
    temperature: float = 0.0
    top_p: float = 1.0
    max_tokens: int = 1200
    model: Optional[str] = None  


@dataclass(frozen=True)
class PipelineResult:
    tests_text: str

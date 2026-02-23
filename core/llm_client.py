import os
import json
import urllib.request
import urllib.error
from dataclasses import dataclass

from core.types import LLMRequest
from core.errors import LLMError


class LLMProvider:
    def generate(self, req: LLMRequest) -> str:
        raise NotImplementedError


@dataclass
class HttpLLMProvider(LLMProvider):
    endpoint: str
    api_key: str

    def generate(self, req: LLMRequest) -> str:
        model = os.getenv("LLM_MODEL", "").strip() or "arcee-ai/trinity-large-preview:free"

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": req.system_prompt},
                {"role": "user", "content": req.user_prompt},
            ],
            "temperature": req.temperature,
            "max_tokens": req.max_tokens,
        }

        data = json.dumps(payload).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost",
            "X-Title": "unit-test-cli-tool",
        }

        request = urllib.request.Request(self.endpoint, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(request, timeout=60) as resp:
                body = resp.read().decode("utf-8", errors="replace")

        except urllib.error.HTTPError as e:
            err_body = ""
            try:
                err_body = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            raise LLMError(f"LLM request failed (HTTP {e.code}). Details: {err_body or str(e)}")

        except Exception as e:
            raise LLMError(f"LLM request failed: {e}")

        try:
            obj = json.loads(body)
        except json.JSONDecodeError:
            raise LLMError("LLM response was not valid JSON")

        choices = obj.get("choices", [])
        if not choices:
            raise LLMError(f"Invalid LLM response: missing choices. Raw: {body[:300]}")

        message = choices[0].get("message", {})
        content = message.get("content")
        if not isinstance(content, str) or not content.strip():
            raise LLMError(f"Invalid LLM response: missing message content. Raw: {body[:300]}")

        return content.strip()


def load_provider_from_env() -> LLMProvider:
    endpoint = os.getenv("LLM_ENDPOINT", "").strip()
    api_key = os.getenv("LLM_API_KEY", "").strip()

    if not endpoint or not api_key:
        raise LLMError("Missing LLM_ENDPOINT or LLM_API_KEY environment variables")

    return HttpLLMProvider(endpoint=endpoint, api_key=api_key)


def call_llm(req: LLMRequest) -> str:
    provider = load_provider_from_env()
    return provider.generate(req)

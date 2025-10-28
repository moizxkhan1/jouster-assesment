"""
LLM client wrapper used by TextAnalyzerService
"""

import os
import json
import time
import re
from typing import Any, Dict

from openai import AsyncOpenAI

from app.core.config import settings
from app.prompts.prompts import COMPREHENSIVE_ANALYSIS_PROMPT
from app.models.schemas import LLMAnalysisResponse
from app.utils.logger import log_llm_request


class LLMClient:
    def __init__(self) -> None:
        api_key = (
            settings.OPENAI_API_KEY
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("GEMINI_API_KEY")
            or ""
        )
        base_url = os.getenv("OPENAI_BASE_URL") or os.getenv("GEMINI_BASE_URL")
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url) if api_key else None
        self.model = (
            settings.OPENAI_MODEL
            or os.getenv("OPENAI_MODEL")
            or os.getenv("GEMINI_MODEL")
            or "gpt-4o-2024-08-06"
        )

    async def analyze_text_comprehensive(self, text: str) -> LLMAnalysisResponse:
        if not self.client:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        prompt = COMPREHENSIVE_ANALYSIS_PROMPT.format(
            text=text[: settings.MAX_TEXT_LENGTH]
        )

        start = time.perf_counter()
        content: str

        try:
            # Prefer JSON mode for stricter structure; fall back if unsupported
            try:
                resp = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Return only a strict JSON object with keys: "
                                "title, summary, sentiment, topics (exactly 3 items)."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0,
                    response_format={"type": "json_object"},
                )
            except Exception:
                resp = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Respond with a JSON object only. Keys: title, summary, "
                                "sentiment (positive|neutral|negative), topics (3 strings)."
                            ),
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0,
                )

            content = (resp.choices[0].message.content or "").strip()
            data = self._parse_json(content)

            topics = data.get("topics") or []
            if not isinstance(topics, list):
                topics = []
            topics = [str(t).strip() for t in topics if str(t).strip()]
            if len(topics) > 3:
                topics = topics[:3]
            while len(topics) < 3:
                topics.append("")

            sentiment = (data.get("sentiment") or "neutral").lower()
            if sentiment not in {"positive", "neutral", "negative"}:
                sentiment = "neutral"

            result = LLMAnalysisResponse.model_validate(
                {
                    "summary": data.get("summary") or "",
                    "title": data.get("title"),
                    "topics": topics,
                    "sentiment": sentiment,
                }
            )

            log_llm_request("comprehensive", len(text), time.perf_counter() - start)
            return result
        except Exception as e:
            raise RuntimeError(f"LLM analysis failed: {e}")

    def _parse_json(self, content: str) -> Dict[str, Any]:
        try:
            fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", content, re.DOTALL)
            if fenced:
                content = fenced.group(1)
            return json.loads(content)
        except Exception:
            # Last resort: attempt to locate the first JSON object in the text
            m = re.search(r"\{[\s\S]*\}", content)
            if m:
                return json.loads(m.group(0))
            return {}


# Global instance
llm_client = LLMClient()

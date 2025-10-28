import sys
import types
import asyncio
from pathlib import Path

# Ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from app.services.text_analyzer import text_analyzer_service
from app.models.schemas import TextAnalysisRequest, LLMAnalysisResponse


class DummyLLM:
    async def analyze_text_comprehensive(self, text: str) -> LLMAnalysisResponse:
        return LLMAnalysisResponse(
            summary="This is a short summary.",
            title="Sample Title",
            topics=["AI", "Work", "Privacy"],
            sentiment="positive",
        )


@pytest.mark.asyncio
async def test_analyze_text_with_mock_llm(monkeypatch):
    # Patch the LLM client on the service instance
    monkeypatch.setattr(text_analyzer_service, "llm_client", DummyLLM())

    req = TextAnalysisRequest(
        text=(
            "Artificial intelligence is changing work. Many worry about privacy, "
            "while others see benefits in productivity and assistance."
        ),
        include_keywords=True,
        include_sentiment=True,
    )

    resp = await text_analyzer_service.analyze_text(req)

    assert resp.summary
    assert resp.metadata.title == "Sample Title"
    assert resp.metadata.sentiment in {"positive", "neutral", "negative"}
    assert len(resp.metadata.topics) == 3
    assert 0.0 <= resp.processing_time <= 10.0
    assert 0.0 <= resp.confidence_score <= 1.0

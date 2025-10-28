"""
Text analysis service - main business logic
"""

import time
from typing import Dict, Any
from app.models.schemas import TextAnalysisRequest, TextAnalysisResponse, TextMetadata
from app.lib.llm_client import llm_client
from app.lib.keyword_extractor import keyword_extractor


class TextAnalyzerService:
    """Main service for text analysis operations"""
    
    def __init__(self):
        self.llm_client = llm_client
        self.keyword_extractor = keyword_extractor
    
    async def analyze_text(self, request: TextAnalysisRequest) -> TextAnalysisResponse:
        """
        Analyze text and return comprehensive results
        
        Args:
            request: Text analysis request
            
        Returns:
            Complete text analysis response
        """
        start_time = time.time()
        
        try:
            # Get comprehensive analysis from LLM (single API call)
            llm_analysis = await self.llm_client.analyze_text_comprehensive(request.text)
            
            # Extract keywords (if requested) - still using non-LLM approach
            keywords = []
            if request.include_keywords:
                keywords = self.keyword_extractor.extract_keywords(request.text)
            
            # Build metadata response
            metadata = TextMetadata(
                title=llm_analysis.title,
                topics=llm_analysis.topics,
                sentiment=llm_analysis.sentiment if request.include_sentiment else "neutral",
                keywords=keywords
            )
            
            processing_time = time.time() - start_time
            confidence = self._compute_confidence(request.text, llm_analysis.summary, metadata)
            
            return TextAnalysisResponse(
                summary=llm_analysis.summary,
                metadata=metadata,
                processing_time=processing_time,
                confidence_score=confidence,
            )
            
        except Exception as e:
            raise Exception(f"Text analysis failed: {str(e)}")

    def _compute_confidence(self, text: str, summary: str, metadata: TextMetadata) -> float:
        """Naive heuristic confidence: structure completeness + input length.
        - base = 0.5 if non-empty summary else 0.2
        - +0.2 if exactly 3 non-empty topics
        - +0.1 if 2+ keywords
        - +0.1 if sentiment in allowed set
        - +0.1 scaled for input length (200-2000 chars)
        """
        score = 0.2
        if summary and len(summary.strip()) > 0:
            score = 0.5

        topics = [t for t in (metadata.topics or []) if isinstance(t, str) and t.strip()]
        if len(topics) == 3:
            score += 0.2

        if isinstance(metadata.keywords, list) and len(metadata.keywords) >= 2:
            score += 0.1

        if metadata.sentiment in {"positive", "neutral", "negative"}:
            score += 0.1

        n = len(text or "")
        # Scale 0..0.1 between 200 and 2000 chars
        if n > 0:
            scaled = max(0.0, min(1.0, (n - 200) / 1800.0)) * 0.1
            score += scaled

        return max(0.0, min(1.0, round(score, 3)))


# Global service instance
text_analyzer_service = TextAnalyzerService()

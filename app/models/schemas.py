"""
Pydantic schemas for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class TextAnalysisRequest(BaseModel):
    """Request schema for text analysis"""
    
    text: str = Field(
        ..., 
        description="The unstructured text to analyze",
        min_length=10,
        max_length=10000
    )
    include_keywords: bool = Field(
        default=True, 
        description="Whether to extract keywords"
    )
    include_sentiment: bool = Field(
        default=True, 
        description="Whether to analyze sentiment"
    )


class TextAnalysisResponse(BaseModel):
    """Response schema for text analysis"""
    
    summary: str = Field(..., description="1-2 sentence summary of the text")
    metadata: "TextMetadata" = Field(..., description="Extracted metadata")
    processing_time: float = Field(..., description="Processing time in seconds")
    confidence_score: float = Field(
        ..., ge=0.0, le=1.0, description="Heuristic confidence score (0.0-1.0)"
    )


class BaseAnalysisData(BaseModel):
    """Base schema for analysis data shared between LLM and final response"""
    
    title: Optional[str] = Field(None, description="Extracted or generated title")
    topics: List[str] = Field(..., description="3 key topics identified")
    sentiment: Literal["positive", "neutral", "negative"] = Field(
        ..., 
        description="Sentiment analysis result"
    )


class LLMAnalysisResponse(BaseAnalysisData):
    """Schema for LLM comprehensive analysis response"""
    
    summary: str = Field(..., description="1-2 sentence summary")


class TextMetadata(BaseAnalysisData):
    """Metadata extracted from text"""
    
    keywords: List[str] = Field(..., description="Top 3 most frequent nouns")


class ErrorResponse(BaseModel):
    """Error response schema"""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")


# Update forward references
TextAnalysisResponse.model_rebuild()

"""
Database models for text analysis
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.database.database import Base


class TextAnalysis(Base):
    """Model for storing text analysis results"""
    
    __tablename__ = "text_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    original_text = Column(Text, nullable=False)
    summary = Column(Text, nullable=False)
    title = Column(String(500), nullable=True)
    topics = Column(JSON, nullable=True)  # Store as JSON array
    sentiment = Column(String(20), nullable=False)
    keywords = Column(JSON, nullable=True)  # Store as JSON array
    processing_time = Column(Float, nullable=False)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<TextAnalysis(id={self.id}, title='{self.title}')>"

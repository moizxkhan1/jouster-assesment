"""
API endpoints for text analysis
"""

import time
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_, text
from app.models.schemas import TextAnalysisRequest, TextAnalysisResponse, ErrorResponse
from app.services.text_analyzer import text_analyzer_service
from app.database.database import get_db
from app.database.models import TextAnalysis
from app.utils.logger import log_request, log_error

router = APIRouter()


@router.post(
    "/analyze",
    response_model=TextAnalysisResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"}
    },
    summary="Analyze Text",
    description="Analyze unstructured text to extract summary, metadata, sentiment, and keywords"
)
async def analyze_text(request: TextAnalysisRequest, db: Session = Depends(get_db)) -> TextAnalysisResponse:
    """
    Analyze text and return comprehensive results including:
    - 1-2 sentence summary
    - Extracted metadata (title, topics)
    - Sentiment analysis
    - Top keywords
    """
    start_time = time.time()
    
    try:
        result = await text_analyzer_service.analyze_text(request)
        
        # Store analysis result in database
        db_analysis = TextAnalysis(
            original_text=request.text,
            summary=result.summary,
            title=result.metadata.title,
            topics=result.metadata.topics,
            sentiment=result.metadata.sentiment,
            keywords=result.metadata.keywords,
            processing_time=result.processing_time,
            confidence_score=result.confidence_score,
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)
        
        # Log successful request
        response_time = time.time() - start_time
        log_request(
            method="POST",
            url="/api/analyze",
            data=request.dict(),
            response_time=response_time
        )
        
        return result
    except Exception as e:
        # Log error
        log_error(e, "text_analysis")
        
        raise HTTPException(
            status_code=500,
            detail=f"Text analysis failed: {str(e)}"
        )


@router.get(
    "/history",
    summary="Get Analysis History",
    description="Get a list of previous text analyses with optional filtering"
)
async def get_analysis_history(
    skip: int = 0,
    limit: int = 20,
    sentiment: str = None,
    keyword: str = None,
    search: str = None,
    db: Session = Depends(get_db)
):
    """Get analysis history with pagination and filtering"""
    try:
        # Build base query
        query = db.query(TextAnalysis)
        
        # Apply filters
        if sentiment and sentiment.lower() in ['positive', 'negative', 'neutral']:
            query = query.filter(TextAnalysis.sentiment == sentiment.lower())
        
        if keyword:
            # Search for keyword in the keywords JSON array using raw SQL
            keyword_lower = keyword.lower()
            query = query.filter(
                text("keywords::text ILIKE :keyword")
            ).params(keyword=f"%{keyword_lower}%")
        
        if search:
            # Search in original text, summary, and title
            # Note: Topics search is complex with JSON, so we'll search in text fields only
            search_term = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    TextAnalysis.original_text.ilike(search_term),
                    TextAnalysis.summary.ilike(search_term),
                    TextAnalysis.title.ilike(search_term)
                )
            )
        
        # Get total count for pagination
        total_count = query.count()
        
        # Apply ordering, pagination and execute
        analyses = query.order_by(TextAnalysis.created_at.desc()).offset(skip).limit(limit).all()
        
        return {
            "analyses": [
                {
                    "id": analysis.id,
                    "title": analysis.title,
                    "summary": analysis.summary,
                    "topics": analysis.topics,
                    "sentiment": analysis.sentiment,
                    "keywords": analysis.keywords,
                    "processing_time": analysis.processing_time,
                    "created_at": analysis.created_at.isoformat() if analysis.created_at else None
                }
                for analysis in analyses
            ],
            "total": total_count,
            "skip": skip,
            "limit": limit,
            "filters": {
                "sentiment": sentiment,
                "keyword": keyword,
                "search": search
            }
        }
    except Exception as e:
        log_error(e, "get_analysis_history")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch analysis history: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health Check",
    description="Check if the API is running"
)
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "service": "text-analysis-api"}

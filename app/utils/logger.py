"""
Simple logging utility for development
"""

import logging
import json
from datetime import datetime
from typing import Dict, Any
from app.core.config import settings


def setup_logger():
    """Setup logger configuration"""
    if settings.DEBUG:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        logging.basicConfig(level=logging.WARNING)


def log_request(method: str, url: str, data: Dict[str, Any] = None, response_time: float = None):
    """Log API requests in development mode"""
    if not settings.DEBUG:
        return
    
    logger = logging.getLogger('api_requests')
    
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'method': method,
        'url': url,
        'response_time_ms': round(response_time * 1000, 2) if response_time else None
    }
    
    if data:
        # Sanitize sensitive data
        sanitized_data = data.copy()
        if 'text' in sanitized_data:
            # Truncate long text for logging
            text = sanitized_data['text']
            if len(text) > 100:
                sanitized_data['text'] = text[:100] + '...'
        
        log_data['request_data'] = sanitized_data
    
    logger.info(f"API Request: {json.dumps(log_data, indent=2)}")


def log_error(error: Exception, context: str = ""):
    """Log errors in development mode"""
    if not settings.DEBUG:
        return
    
    logger = logging.getLogger('errors')
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)


def log_llm_request(prompt_type: str, text_length: int, response_time: float = None):
    """Log LLM API requests"""
    if not settings.DEBUG:
        return
    
    logger = logging.getLogger('llm_requests')
    
    log_data = {
        'timestamp': datetime.now().isoformat(),
        'prompt_type': prompt_type,
        'text_length': text_length,
        'response_time_ms': round(response_time * 1000, 2) if response_time else None
    }
    
    logger.info(f"LLM Request: {json.dumps(log_data, indent=2)}")


# Initialize logger on import
setup_logger()

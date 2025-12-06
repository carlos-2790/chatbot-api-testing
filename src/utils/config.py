"""
Configuration module for chatbot API testing.
Loads settings from environment variables with sensible defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Central configuration class for the testing framework."""
    
    # API Configuration
    API_URL = os.getenv(
        'API_URL',
        'https://magicloops.dev/api/loop/7e391b7e-f45a-49ec-bd71-bd23b9ad711e/run'
    )
    
    # Quality Threshold
    QUALITY_THRESHOLD = float(os.getenv('QUALITY_THRESHOLD', '0.85'))
    
    # Timeout settings
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '10'))
    REQUEST_RETRY_COUNT = int(os.getenv('REQUEST_RETRY_COUNT', '3'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Paths
    PROJECT_ROOT = Path(__file__).parent.parent.parent
    DATA_DIR = PROJECT_ROOT / 'data'
    REPORTS_DIR = PROJECT_ROOT / 'reports'
    
    # Semantic validation settings
    SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'  # Fast and efficient model
    SIMILARITY_THRESHOLD = 0.5  # Minimum semantic similarity score
    
    @classmethod
    def validate(cls):
        """Validate configuration values."""
        if not 0.0 <= cls.QUALITY_THRESHOLD <= 1.0:
            raise ValueError(f"QUALITY_THRESHOLD must be between 0.0 and 1.0, got {cls.QUALITY_THRESHOLD}")
        
        if cls.API_TIMEOUT <= 0:
            raise ValueError(f"API_TIMEOUT must be positive, got {cls.API_TIMEOUT}")
        
        if cls.REQUEST_RETRY_COUNT < 0:
            raise ValueError(f"REQUEST_RETRY_COUNT must be non-negative, got {cls.REQUEST_RETRY_COUNT}")
        
        return True

# Validate configuration on import
Config.validate()

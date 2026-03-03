"""
Configuration and environment management for Market State Engine.
Centralized config to ensure consistency across components.
"""

import os
from dataclasses import dataclass
from typing import Optional, Dict, Any
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class ExchangeConfig:
    """Configuration for exchange connections"""
    name: str
    api_key: str
    api_secret: str
    sandbox_mode: bool = True
    rate_limit: int = 1000  # requests per minute
    retry_count: int = 3
    
@dataclass
class FeatureConfig:
    """Configuration for feature engineering"""
    timeframes: Dict[str, str] = None  # e.g., {'1h': '1h', '4h': '4h', '1d': '1d'}
    feature_window_sizes: Dict[str, int] = None  # e.g., {'short': 20, 'medium': 50, 'long': 200}
    normalization_method: str = 'zscore'  # 'zscore', 'minmax', 'robust'
    
@dataclass
class FirebaseConfig:
    """Configuration for Firebase/Firestore"""
    project_id: str
    credentials_path: Optional[str] = None
    collection_prefix: str = 'trading_engine'
    
class ConfigManager:
    """Central configuration manager with validation"""
    
    def __init__(self):
        self._validate_env()
        self.exchange = self._load_exchange_config()
        self.features = self._load_feature_config()
        self.firebase = self._load_firebase_config()
        self._init_firebase()
        
    def _validate_env(self) -> None:
        """Validate required environment variables"""
        required_vars = [
            'EXCHANGE_NAME',
            'EXCHANGE_API_KEY',
            'EXCHANGE_API_SECRET',
            'FIREBASE_PROJECT_ID'
        ]
        
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {missing}")
            
    def _load_exchange_config(self) -> ExchangeConfig:
        """Load exchange configuration from environment"""
        return ExchangeConfig(
            name=os.getenv('EXCHANGE_NAME', 'binance'),
            api_key=os.getenv('EXCHANGE_API_KEY'),
            api_secret=os.getenv('EXCHANGE_API_SECRET'),
            sandbox_mode=os.getenv('SANDBOX_MODE', 'True').lower() == 'true',
            rate_limit=int(os.getenv('RATE_LIMIT', '1000')),
            retry_count=int(os.getenv('RETRY_COUNT', '3'))
        )
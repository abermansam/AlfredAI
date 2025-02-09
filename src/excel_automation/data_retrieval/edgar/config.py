"""
Configuration for EDGAR API access
"""

import os
from dataclasses import dataclass

@dataclass
class EdgarConfig:
    """EDGAR API configuration"""
    user_agent: str = os.getenv(
        "EDGAR_USER_AGENT", 
        "alfredAI sam.aberman@gmail.com"
    )
    base_url: str = "https://data.sec.gov/api/xbrl/companyfacts"
    company_search_url: str = "https://www.sec.gov/files/company_tickers.json"
    rate_limit_sleep: int = 0.1 
"""
EDGAR data models
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class EdgarQuery:
    """Represents a parsed EDGAR query"""
    company_name: str
    ticker: Optional[str]
    cik: Optional[str]
    filing_type: str
    filing_date: Optional[datetime]
    metrics: List[str] 
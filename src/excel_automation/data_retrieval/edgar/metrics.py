"""
EDGAR metric mappings and utilities
"""

from typing import Dict, Optional

# Mapping of common names to XBRL tags
METRIC_MAPPINGS = {
    "total assets": "Assets",
    "total liabilities": "Liabilities",
    "net income": "NetIncomeLoss",
    "revenue": "Revenues",
    "operating income": "OperatingIncomeLoss",
    "cash and equivalents": "CashAndCashEquivalentsAtCarryingValue",
    "total equity": "StockholdersEquity",
    "earnings per share": "EarningsPerShareBasic",
    "gross profit": "GrossProfit",
    "operating expenses": "OperatingExpenses",
}

def normalize_metric_name(metric: str) -> Optional[str]:
    """Convert common metric names to XBRL tags"""
    metric = metric.lower().strip()
    return METRIC_MAPPINGS.get(metric)

def get_metric_value(filing_data: Dict, metric_tag: str, filing_date: Optional[str] = None) -> Optional[float]:
    """Extract metric value from filing data"""
    try:
        # Navigate to US GAAP metrics
        us_gaap = filing_data.get("facts", {}).get("us-gaap", {})
        metric_data = us_gaap.get(metric_tag, {}).get("units", {}).get("USD", [])
        
        if not metric_data:
            return None
        
        if filing_date:
            # Find exact date match
            for entry in metric_data:
                if entry.get("end") == filing_date:
                    return entry.get("val")
        else:
            # Get most recent value
            sorted_entries = sorted(metric_data, key=lambda x: x.get("end", ""), reverse=True)
            if sorted_entries:
                return sorted_entries[0].get("val")
        
        return None
    except Exception:
        return None 
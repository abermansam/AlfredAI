# EDGAR Data Retrieval Module

## Overview
The EDGAR module provides comprehensive functionality for retrieving and parsing financial data from SEC's EDGAR database. It includes configuration, data models, metric mappings, and natural language processing capabilities.

## Components

### Config (`config.py`)
Configuration class for EDGAR API access:
```python
class EdgarConfig:
    def __init__(self, user_agent: str):
        """Initialize EDGAR configuration
        
        Args:
            user_agent: Email address for SEC EDGAR access
        """
        self.user_agent = user_agent
        self.base_url = "https://www.sec.gov"
        self.company_tickers_url = f"{self.base_url}/files/company_tickers.json"
```

### Models (`models.py`)
Data models for EDGAR queries and responses:
```python
@dataclass
class EdgarQuery:
    """Represents a parsed EDGAR query"""
    company_name: str
    ticker: str
    filing_type: str
    filing_date: str
    metrics: List[str]

@dataclass
class EdgarFiling:
    """Represents an EDGAR filing"""
    cik: str
    accession_number: str
    filing_type: str
    filing_date: str
    data: Dict
```

### Metrics (`metrics.py`)
Financial metric mappings and utilities:
```python
# Common financial metrics mapped to XBRL tags
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

def get_metric_value(filing_data: Dict, 
                    metric_tag: str, 
                    filing_date: Optional[str] = None) -> Optional[float]:
    """Extract metric value from filing data"""
```

### Prompts (`prompts.py`)
LLM prompts for parsing EDGAR commands:
```python
EDGAR_COMMAND_PARSE_PROMPT = """
You are a financial data assistant. Parse the following command into structured data:
{command}

Return a JSON object with:
- company_name: Full company name
- ticker: Stock ticker symbol
- filing_type: SEC filing type (e.g., "10-K", "10-Q")
- filing_date: Date or "latest"
- metrics: List of requested financial metrics

Example response:
{
    "company_name": "Apple Inc.",
    "ticker": "AAPL",
    "filing_type": "10-K",
    "filing_date": "latest",
    "metrics": ["revenue", "net income"]
}
"""
```

### Retriever (`retriever.py`)
Main class for EDGAR data retrieval:
```python
class EdgarRetriever(DataRetriever):
    def __init__(self, config: EdgarConfig, llm_provider: str = "openai"):
        """Initialize EDGAR retriever with config and LLM provider"""
    
    def test_connection(self) -> bool:
        """Test EDGAR API connection"""
    
    def get_company_info(self, ticker: str) -> Dict:
        """Get company CIK and details
        
        Args:
            ticker: Company stock ticker
            
        Returns:
            Dict with company info including CIK
        """
    
    def parse_command(self, command: str) -> EdgarQuery:
        """Parse natural language command into structured query
        
        Args:
            command: Natural language command
            
        Returns:
            EdgarQuery with parsed information
        """
    
    def fetch_filing(self, cik: str, filing_type: str) -> Dict:
        """Fetch specific SEC filing
        
        Args:
            cik: Company CIK number
            filing_type: Type of filing (10-K, 10-Q)
            
        Returns:
            Filing data in JSON format
        """
    
    def extract_metrics(self, 
                       filing_data: Dict, 
                       metrics: List[str],
                       filing_date: Optional[str] = None) -> List[FinancialData]:
        """Extract requested metrics from filing
        
        Args:
            filing_data: Raw filing data
            metrics: List of metrics to extract
            filing_date: Optional specific date
            
        Returns:
            List of FinancialData objects
        """
```

## Usage Examples

### Basic Usage
```python
# Initialize retriever
config = EdgarConfig(user_agent="your.email@example.com")
retriever = EdgarRetriever(config, llm_provider="ollama")

# Natural language query
command = "Get Apple's latest 10-K and show revenue and net income"
query = retriever.parse_command(command)

# Get company info and filing
company = retriever.get_company_info(query.ticker)
filing = retriever.fetch_filing(company["cik"], query.filing_type)

# Extract metrics
results = retriever.extract_metrics(filing, query.metrics)
```

### Working with Specific Metrics
```python
# Get metric value from filing
from excel_automation.data_retrieval.edgar.metrics import get_metric_value

value = get_metric_value(
    filing_data=filing,
    metric_tag="Assets",
    filing_date="2023-09-30"
)

# Convert common name to XBRL tag
from excel_automation.data_retrieval.edgar.metrics import normalize_metric_name

xbrl_tag = normalize_metric_name("total assets")  # Returns "Assets"
```

## Error Handling
The module implements comprehensive error handling for:
- Network connectivity issues
- Invalid company tickers
- Missing filing data
- Invalid metric names
- Rate limiting
- JSON parsing errors

## Rate Limiting
The SEC EDGAR system has rate limiting requirements:
- 10 requests per second
- Must include valid user agent (email)
- Automatic retry with backoff implemented 
# EDGAR Data Retrieval

## Overview
The EDGAR module provides functionality to retrieve and parse financial data from SEC's EDGAR database. It supports natural language queries and extracts standardized financial metrics.

## Components

### EdgarRetriever
Main class for EDGAR data retrieval:
```python
class EdgarRetriever(DataRetriever):
    def test_connection(self) -> bool:
        """Test EDGAR API connection"""
    
    def get_company_info(self, ticker: str) -> Dict:
        """Get company CIK and details"""
    
    def parse_command(self, command: str) -> EdgarQuery:
        """Parse natural language command"""
    
    def fetch_filing(self, cik: str, filing_type: str) -> Dict:
        """Fetch specific SEC filing"""
    
    def extract_metrics(self, filing_data: Dict, metrics: List[str]) -> List[FinancialData]:
        """Extract requested metrics from filing"""
```

### Supported Metrics
Common financial metrics mapped to XBRL tags:
- Total Assets (`Assets`)
- Revenue (`Revenues`)
- Net Income (`NetIncomeLoss`)
- Operating Income (`OperatingIncomeLoss`)
- And more...

## Usage Example
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
"""
EDGAR command parsing prompts
"""

EDGAR_COMMAND_PARSE_PROMPT = """You are a financial data assistant. Parse the following command into structured data for retrieving financial information from SEC EDGAR.

Guidelines:
1. Extract company name and ticker if provided
2. Identify the filing type (10-K, 10-Q, etc.)
3. Look for date specifications or use "latest"
4. List all financial metrics requested
5. Standardize metric names (e.g., "total assets", "net income", "revenue")

The response must be valid JSON with this structure:
{{
    "company_name": "Full company name",
    "ticker": "SYMBOL",
    "filing_type": "10-K or 10-Q",
    "filing_date": "YYYY-MM-DD or latest",
    "metrics": ["metric1", "metric2", ...]
}}

Example command:
"Get Apple's latest 10-K and show revenue and net income"

Example response:
{{
    "company_name": "Apple Inc.",
    "ticker": "AAPL",
    "filing_type": "10-K",
    "filing_date": "latest",
    "metrics": ["revenue", "net income"]
}}

Command to parse:
{command}

Provide only the JSON response, no additional text.""" 
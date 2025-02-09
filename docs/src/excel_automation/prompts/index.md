# Prompts Module

## Overview
The prompts module contains standardized prompt templates for different LLM interactions in the system. It provides consistent prompting patterns for financial data extraction and command parsing.

## Components

### Financial Extraction (`financial_extraction.py`)
Contains prompts for extracting financial data from unstructured text:

```python
FINANCIAL_EXTRACTION_PROMPT = """
You are a financial data extraction assistant. Extract financial metrics from the following text:
{text}

Return a JSON array of financial metrics with:
- category: Type of metric (revenue, profit, etc.)
- value: Numeric value
- unit: Currency unit
- date: Date if mentioned
- confidence: Extraction confidence (0-1)

Example response:
[
    {
        "category": "revenue",
        "value": 1200000,
        "unit": "USD",
        "date": "2024-Q2",
        "confidence": 0.95
    }
]
"""
```

### EDGAR Command Parsing (`edgar_command.py`)
Contains prompts for parsing natural language commands into EDGAR queries:

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

## Usage

### Financial Data Extraction
```python
from excel_automation.prompts.financial_extraction import FINANCIAL_EXTRACTION_PROMPT
from excel_automation.data_retrieval.providers import get_llm_provider

# Initialize LLM provider
provider = get_llm_provider("ollama")

# Format prompt with text
text = "Q2 2024 revenue was $1.2M with operating expenses of $800K"
prompt = FINANCIAL_EXTRACTION_PROMPT.format(text=text)

# Get structured response
response = provider.complete(prompt)
```

### EDGAR Command Parsing
```python
from excel_automation.prompts.edgar_command import EDGAR_COMMAND_PARSE_PROMPT
from excel_automation.data_retrieval.providers import get_llm_provider

# Initialize LLM provider
provider = get_llm_provider("ollama")

# Format prompt with command
command = "Get Apple's latest 10-K and show revenue and net income"
prompt = EDGAR_COMMAND_PARSE_PROMPT.format(command=command)

# Get structured response
response = provider.complete(prompt)
```

## Design Principles

### Prompt Structure
- Clear role definition for the LLM
- Specific output format requirements
- Example responses included
- Consistent JSON structures

### Integration Points
- Works with any LLM provider
- Supports both OpenAI and Ollama
- Consistent with data models
- Standardized response formats

### Best Practices
1. Use template strings for dynamic content
2. Include example responses in prompts
3. Specify clear output formats
4. Define LLM role explicitly
5. Keep prompts focused and specific

## Response Formats

### Financial Extraction
Returns an array of financial metrics:
```json
[
    {
        "category": "string",
        "value": number,
        "unit": "string",
        "date": "string",
        "confidence": number
    }
]
```

### EDGAR Command Parsing
Returns a structured query object:
```json
{
    "company_name": "string",
    "ticker": "string",
    "filing_type": "string",
    "filing_date": "string",
    "metrics": ["string"]
}
``` 
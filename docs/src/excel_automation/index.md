# Excel Automation Package

## Overview
The Excel Automation package provides a comprehensive framework for automating financial data retrieval, processing, and Excel report generation. It combines natural language processing, financial data extraction, and automated report generation.

## Package Structure
```
excel_automation/
├── data_retrieval/           # Core data retrieval functionality
│   ├── base.py              # Base classes and interfaces
│   ├── edgar/               # SEC EDGAR integration
│   │   ├── config.py        # EDGAR configuration
│   │   ├── metrics.py       # Financial metrics mapping
│   │   ├── models.py        # Data models
│   │   ├── prompts.py       # LLM prompts
│   │   └── retriever.py     # Main EDGAR retriever
│   └── providers/           # LLM providers
│       └── llm.py           # OpenAI and Ollama implementations
├── prompts/                 # LLM prompt templates
│   ├── edgar_command.py     # EDGAR command parsing prompts
│   └── financial_extraction.py  # Financial data extraction prompts
└── __init__.py             # Package initialization
```

## Core Components

### Data Retrieval (`data_retrieval/`)
The foundation for all data retrieval operations:
- Base classes for data retrieval and standardization
- Financial data models and validation
- Integration with various data sources
- [Detailed Documentation](data_retrieval/index.md)

### EDGAR Integration (`data_retrieval/edgar/`)
SEC EDGAR data retrieval and processing:
- Company information lookup
- Filing retrieval (10-K, 10-Q)
- Financial metric extraction
- [Detailed Documentation](data_retrieval/edgar/index.md)

### LLM Providers (`data_retrieval/providers/`)
Language model integration for natural language processing:
- OpenAI integration
- Local Ollama support
- Standardized interface
- [Detailed Documentation](data_retrieval/providers/index.md)

### Prompts (`prompts/`)
LLM prompt templates and utilities:
- Financial data extraction prompts
- EDGAR command parsing
- Standardized response formats
- [Detailed Documentation](prompts/index.md)

## Main Workflows

### 1. Natural Language Query Processing
```python
from excel_automation.data_retrieval.edgar import EdgarRetriever, EdgarConfig
from excel_automation.prompts.edgar_command import EDGAR_COMMAND_PARSE_PROMPT

# Initialize components
config = EdgarConfig(user_agent="your.email@example.com")
retriever = EdgarRetriever(config, llm_provider="ollama")

# Process natural language query
command = "Get Apple's latest 10-K and show revenue and net income"
query = retriever.parse_command(command)
```

### 2. Financial Data Retrieval
```python
# Get company information
company = retriever.get_company_info(query.ticker)

# Fetch and process filing
filing = retriever.fetch_filing(company["cik"], query.filing_type)
results = retriever.extract_metrics(filing, query.metrics)
```

### 3. Data Extraction from Text
```python
from excel_automation.prompts.financial_extraction import FINANCIAL_EXTRACTION_PROMPT
from excel_automation.data_retrieval.providers import get_llm_provider

# Extract financial data from text
provider = get_llm_provider("ollama")
text = "Q2 2024 revenue was $1.2M"
results = provider.complete(FINANCIAL_EXTRACTION_PROMPT.format(text=text))
```

## Integration Points

### With External Systems
- SEC EDGAR API integration
- LLM provider APIs (OpenAI, Ollama)
- Excel file handling

### Between Components
- Data Retriever → LLM Provider
- LLM Provider → Prompts
- EDGAR Retriever → Base Retriever

## Configuration

### EDGAR Configuration
```python
class EdgarConfig:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.base_url = "https://www.sec.gov"
```

### LLM Provider Configuration
```python
# OpenAI
provider = get_llm_provider("openai", api_key="your-api-key")

# Ollama
provider = get_llm_provider(
    "ollama",
    model="mistral",
    base_url="http://localhost:11434"
)
```

## Best Practices

1. Data Retrieval
   - Always validate retrieved data
   - Handle rate limiting appropriately
   - Include proper error handling

2. LLM Integration
   - Use standardized prompt templates
   - Validate JSON responses
   - Handle model-specific errors

3. Configuration
   - Use environment variables for sensitive data
   - Configure rate limiting appropriately
   - Set proper timeouts

## Error Handling
The package implements comprehensive error handling for:
- Network connectivity issues
- API rate limiting
- Invalid data formats
- LLM response validation
- File I/O operations 
# LLM Providers Module

## Overview
The providers module implements different Large Language Model (LLM) backends for natural language processing. It provides a unified interface for both cloud-based (OpenAI) and local (Ollama) LLM implementations.

## Components

### OpenAIProvider
Cloud-based LLM provider using OpenAI's API:
```python
class OpenAIProvider:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI provider
        
        Args:
            api_key: Optional API key (defaults to OPENAI_API_KEY env var)
        """
    
    def complete(self, prompt: str) -> str:
        """Get completion from OpenAI
        
        Args:
            prompt: Input prompt for completion
            
        Returns:
            JSON-formatted string response
            
        Raises:
            Exception: On API error or invalid response
        """
```

### OllamaProvider
Local LLM provider using Ollama:
```python
class OllamaProvider:
    def __init__(self, 
                 model: str = "mistral",
                 base_url: str = "http://localhost:11434",
                 temperature: float = 0.1):
        """Initialize Ollama provider
        
        Args:
            model: Model name to use (default: mistral)
            base_url: Ollama server URL
            temperature: Sampling temperature (0-1)
        """
    
    def complete(self, prompt: str) -> str:
        """Get completion using LangChain
        
        Args:
            prompt: Input prompt for completion
            
        Returns:
            JSON-formatted string response
            
        Raises:
            ValueError: If response is not valid JSON
            Exception: On connection or model errors
        """
```

### Factory Function
```python
def get_llm_provider(provider: str = "openai", **kwargs) -> OpenAIProvider | OllamaProvider:
    """Get LLM provider instance
    
    Args:
        provider: Provider type ("openai" or "ollama")
        **kwargs: Provider-specific configuration
        
    Returns:
        Configured LLM provider instance
        
    Raises:
        ValueError: For unsupported provider types
    """
```

## Configuration

### OpenAI Configuration
- Environment Variables:
  - `OPENAI_API_KEY`: API key for authentication
- Default Settings:
  - Model: gpt-3.5-turbo
  - Temperature: 0.1
  - System prompt: Financial data assistant

### Ollama Configuration
- Requirements:
  - Local Ollama installation
  - Running Ollama server
- Default Settings:
  - Model: mistral
  - Server URL: http://localhost:11434
  - Temperature: 0.1
  - System prompt: Financial data assistant

## Usage Examples

### Using OpenAI
```python
# Initialize with environment variable
provider = get_llm_provider("openai")

# Or with explicit API key
provider = get_llm_provider("openai", api_key="your-api-key")

# Get completion
response = provider.complete("Parse this financial command: Get Apple's revenue")
```

### Using Ollama
```python
# Initialize with defaults
provider = get_llm_provider("ollama")

# Or with custom configuration
provider = get_llm_provider(
    "ollama",
    model="llama2",
    base_url="http://localhost:11434",
    temperature=0.2
)

# Get completion
response = provider.complete("Extract metrics from: Q4 revenue was $1.2M")
```

## Response Format
All providers return JSON-formatted strings with standardized structure:
```json
{
    "company_name": "Company name",
    "ticker": "Stock ticker",
    "filing_type": "Filing type",
    "filing_date": "Date or latest",
    "metrics": ["List", "of", "metrics"]
}
```

## Error Handling
The module implements error handling for:
- API authentication errors
- Connection issues
- Invalid responses
- JSON parsing errors
- Rate limiting
- Model-specific errors

## Implementation Details

### LangChain Integration
The OllamaProvider uses LangChain for:
- Prompt templating
- Chain composition
- Response parsing
- Error handling

### JSON Validation
Both providers ensure valid JSON responses:
1. Attempt direct JSON parsing
2. Extract JSON from text if needed
3. Validate against expected schema
4. Raise appropriate errors

## Dependencies
- openai>=1.12.0
- langchain>=0.1.0
- langchain-core>=0.1.0
- langchain-ollama>=0.0.1 
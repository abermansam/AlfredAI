# LLM Providers

## Overview
The LLM providers module handles natural language processing using different LLM backends. It currently supports OpenAI and Ollama for local inference.

## Components

### OpenAIProvider
```python
class OpenAIProvider:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with optional API key"""
    
    def complete(self, prompt: str) -> str:
        """Get completion from OpenAI"""
```

### OllamaProvider
```python
class OllamaProvider:
    def __init__(self, 
                 model: str = "mistral",
                 base_url: str = "http://localhost:11434",
                 temperature: float = 0.1):
        """Initialize Ollama provider"""
    
    def complete(self, prompt: str) -> str:
        """Get completion using LangChain"""
```

## Configuration
### OpenAI
- Uses environment variable `OPENAI_API_KEY` or passed key
- Default model: gpt-3.5-turbo
- Temperature: 0.1

### Ollama
- Default model: mistral
- Default URL: http://localhost:11434
- Temperature: 0.1
- Requires local Ollama installation

## Usage Example
```python
# Using OpenAI
provider = get_llm_provider("openai")
result = provider.complete("Parse financial command...")

# Using Ollama
provider = get_llm_provider(
    "ollama",
    model="llama2",
    temperature=0.2
)
result = provider.complete("Parse financial command...")
``` 
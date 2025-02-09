# LLM Providers Module

## Overview
The LLM providers module implements different Large Language Model backends with a unified interface.

## Components

### OpenAIProvider
```python
class OpenAIProvider:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI provider
        
        Args:
            api_key: Optional API key (defaults to env var)
        """
    
    def complete(self, prompt: str) -> str:
        """Get completion from OpenAI
        
        Args:
            prompt: Input prompt
            
        Returns:
            Completion response
        """
```

### OllamaProvider
```python
class OllamaProvider:
    def __init__(self, 
                 model: str = "mistral",
                 base_url: str = "http://localhost:11434",
                 temperature: float = 0.1):
        """Initialize Ollama provider
        
        Args:
            model: Model name
            base_url: Ollama server URL
            temperature: Sampling temperature
        """
    
    def complete(self, prompt: str) -> str:
        """Get completion using LangChain"""
```

### Factory Function
```python
def get_llm_provider(provider: str = "openai", 
                    **kwargs) -> OpenAIProvider | OllamaProvider:
    """Get configured LLM provider instance"""
```

## Provider-Specific Features

### OpenAI Features
- GPT-3.5-turbo model support
- API key management
- Rate limiting handling
- Error retry logic

### Ollama Features
- Local model support
- Multiple model options
- Temperature control
- Custom base URL

## Common Functionality
- JSON response validation
- Error handling
- Prompt templating
- Response parsing 
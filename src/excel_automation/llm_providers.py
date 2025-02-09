"""
LLM Provider Interface
"""

from abc import ABC, abstractmethod
from typing import Optional
import os
from loguru import logger

class LLMProvider(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        """Get completion from LLM"""
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None):
        import openai
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI()
        
    def complete(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a financial data assistant that parses commands into structured JSON data."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.1  # Lower temperature for more consistent parsing
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting LLM completion: {str(e)}")
            raise

def get_llm_provider(provider: str = "openai") -> LLMProvider:
    """Get LLM provider instance"""
    if provider == "openai":
        return OpenAIProvider()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}") 
"""
LLM providers for text completion
"""

from typing import Optional
import os
from loguru import logger
import json
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

class OpenAIProvider:
    """OpenAI completion provider"""
    
    def __init__(self, api_key: Optional[str] = None):
        import openai
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = openai.OpenAI()
    
    def complete(self, prompt: str) -> str:
        """Get completion from OpenAI"""
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
                temperature=0.1
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting OpenAI completion: {str(e)}")
            raise

class OllamaProvider:
    """Ollama completion provider using LangChain"""
    
    def __init__(self, 
                 model: str = "mistral", 
                 base_url: str = "http://localhost:11434",
                 temperature: float = 0.1):
        """Initialize Ollama provider with LangChain"""
        try:
            self.llm = OllamaLLM(
                model=model,
                base_url=base_url,
                temperature=temperature
            )
            
            # Create a prompt template
            self.prompt_template = ChatPromptTemplate.from_messages([
                ("system", "You are a financial data assistant that parses commands into structured JSON data."),
                ("user", "{input}")
            ])
            
            # Create the chain
            self.chain = self.prompt_template | self.llm | StrOutputParser()
            
        except Exception as e:
            logger.error(f"Error initializing Ollama provider: {str(e)}")
            raise
        
    def complete(self, prompt: str) -> str:
        """Get completion using LangChain"""
        try:
            # Execute the chain
            response = self.chain.invoke({"input": prompt})
            
            # Validate JSON response
            try:
                # Try parsing to ensure it's valid JSON
                json.loads(response)
                return response
            except json.JSONDecodeError:
                # If not valid JSON, try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    # Validate the extracted JSON
                    json.loads(json_str)
                    return json_str
                raise ValueError("Response is not valid JSON")
            
        except Exception as e:
            logger.error(f"Error getting Ollama completion: {str(e)}")
            raise

def get_llm_provider(provider: str = "openai", **kwargs) -> OpenAIProvider | OllamaProvider:
    """Get LLM provider instance"""
    if provider == "openai":
        return OpenAIProvider(**kwargs)
    elif provider == "ollama":
        return OllamaProvider(**kwargs)
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}") 
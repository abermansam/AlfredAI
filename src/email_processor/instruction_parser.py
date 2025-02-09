"""
Instruction Parser Module

Analyzes email content using LLMs to extract actionable Excel-related tasks.
"""

from typing import Dict, Optional, Union
import json
from loguru import logger
from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def analyze_text(self, prompt: str) -> str:
        pass

class OllamaProvider(LLMProvider):
    """Ollama LLM provider implementation"""
    
    def __init__(self, model_name: str = "llama2"):
        try:
            import ollama
            self.ollama = ollama
            self.model_name = model_name
        except ImportError:
            raise ImportError("Please install ollama package: pip install ollama")

    def analyze_text(self, prompt: str) -> str:
        response = self.ollama.generate(
            model=self.model_name,
            prompt=prompt
        )
        return response['response']

class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation"""
    
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        try:
            import openai
            self.openai = openai
            self.openai.api_key = api_key
            self.model_name = model_name
        except ImportError:
            raise ImportError("Please install openai package: pip install openai")

    def analyze_text(self, prompt: str) -> str:
        response = self.openai.ChatCompletion.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a financial model assistant that analyzes emails to extract Excel-related tasks."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

class InstructionParser:
    """
    Parses email content to extract Excel-related instructions using LLMs.
    """
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize the instruction parser.
        
        Args:
            llm_provider: LLM provider instance (Ollama or OpenAI)
        """
        self.llm = llm_provider
        
    def parse_email(self, email_data: Dict) -> Optional[Dict]:
        """
        Parse email content to determine if it contains Excel-related tasks.
        
        Args:
            email_data: Email data dictionary from GmailConnector
            
        Returns:
            Optional[Dict]: Structured task information if found, None otherwise
        """
        try:
            # Construct prompt for LLM
            prompt = self._construct_prompt(email_data)
            
            # Get LLM analysis
            response = self.llm.analyze_text(prompt)
            
            # Parse LLM response
            task_info = self._parse_llm_response(response)
            
            if task_info and task_info['is_excel_task']:
                return task_info
            return None
            
        except Exception as e:
            logger.error(f"Error parsing email instructions: {str(e)}")
            return None
    
    def _construct_prompt(self, email_data: Dict) -> str:
        """Construct prompt for LLM analysis."""
        return f"""
        Analyze the following email to determine if it contains instructions for Excel/financial model work.
        If it does, extract the specific tasks and requirements.
        
        Subject: {email_data['subject']}
        Body: {email_data['body']}
        Attachments: {[att['filename'] for att in email_data['attachments']]}
        
        Please provide a JSON response with the following structure:
        {{
            "is_excel_task": boolean,
            "task_type": "edit_existing" or "create_new" or "none",
            "model_name": string or null,
            "required_changes": [list of specific changes] or null,
            "use_attachment": boolean,
            "attachment_name": string or null,
            "priority": "high" or "medium" or "low",
            "confidence_score": float (0-1)
        }}
        """
    
    def _parse_llm_response(self, response: str) -> Dict:
        """Parse LLM response into structured task information."""
        try:
            # Extract JSON from response (handle potential text wrapping)
            json_str = response.strip()
            if '```json' in json_str:
                json_str = json_str.split('```json')[1].split('```')[0]
            
            task_info = json.loads(json_str)
            return task_info
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            return None 
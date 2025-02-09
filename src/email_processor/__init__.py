# Email processor module initialization 
from .gmail_connector import GmailConnector
from .instruction_parser import InstructionParser, OllamaProvider, OpenAIProvider

__all__ = ['GmailConnector', 'InstructionParser', 'OllamaProvider', 'OpenAIProvider'] 
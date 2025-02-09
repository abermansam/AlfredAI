"""
Tests for LLM providers
"""

import pytest
from excel_automation.data_retrieval.providers import OpenAIProvider, OllamaProvider, get_llm_provider
import json
from unittest.mock import patch, MagicMock

class TestLLMProviders:
    def test_provider_selection(self):
        """Test provider factory function"""
        openai_provider = get_llm_provider("openai")
        assert isinstance(openai_provider, OpenAIProvider)
        
        ollama_provider = get_llm_provider("ollama")
        assert isinstance(ollama_provider, OllamaProvider)
        
        with pytest.raises(ValueError):
            get_llm_provider("unsupported")
    
    def test_openai_provider(self, mocker):
        """Test OpenAI provider"""
        mock_openai = mocker.patch('openai.OpenAI')
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "company_name": "Apple Inc.",
            "ticker": "AAPL"
        })
        mock_client.chat.completions.create.return_value = mock_response
        
        provider = get_llm_provider("openai")
        response = provider.complete("test prompt")
        
        parsed = json.loads(response)
        assert parsed["company_name"] == "Apple Inc."
        assert parsed["ticker"] == "AAPL"
    
    def test_ollama_provider(self, mocker):
        """Test Ollama provider"""
        with patch('excel_automation.data_retrieval.providers.llm.OllamaLLM') as mock_ollama:
            mock_chain = MagicMock()
            mock_chain.invoke.return_value = json.dumps({
                "company_name": "Apple Inc.",
                "ticker": "AAPL"
            })
            
            provider = get_llm_provider("ollama")
            provider.chain = mock_chain
            
            response = provider.complete("test prompt")
            parsed = json.loads(response)
            
            assert parsed["company_name"] == "Apple Inc."
            assert parsed["ticker"] == "AAPL"
    
    def test_invalid_json_handling(self):
        """Test handling of invalid JSON responses"""
        provider = OllamaProvider()
        provider.chain = MagicMock()
        
        # Test completely invalid response
        provider.chain.invoke.return_value = "Not JSON at all"
        with pytest.raises(ValueError, match="Response is not valid JSON"):
            provider.complete("test prompt")
        
        # Test response with extractable JSON
        provider.chain.invoke.return_value = "Some text { \"key\": \"value\" } more text"
        response = provider.complete("test prompt")
        assert json.loads(response)["key"] == "value" 
"""
Tests for the email processor module
"""

import pytest
from email_processor import GmailConnector, InstructionParser, OllamaProvider, OpenAIProvider
from unittest.mock import Mock, patch, MagicMock
import json
import base64

# Sample test data
SAMPLE_EMAIL_PAYLOAD = {
    'headers': [
        {'name': 'Subject', 'value': 'Update Financial Model'},
        {'name': 'From', 'value': 'sender@example.com'},
        {'name': 'Date', 'value': '2024-03-20'},
    ],
    'parts': [
        {
            'mimeType': 'text/plain',
            'body': {
                'data': base64.b64encode(b'Please update the revenue projections in Q2_Model.xlsx').decode()
            }
        },
        {
            'filename': 'Q2_Model.xlsx',
            'mimeType': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'body': {
                'attachmentId': 'abc123',
                'data': base64.b64encode(b'mock_excel_data').decode()
            }
        }
    ]
}

SAMPLE_EMAIL_DATA = {
    'id': '12345',
    'threadId': '12345',
    'payload': SAMPLE_EMAIL_PAYLOAD
}

class TestGmailConnector:
    @pytest.fixture
    def gmail_connector(self):
        with patch('email_processor.gmail_connector.build') as mock_build:
            connector = GmailConnector()
            connector.service = Mock()
            yield connector

    def test_authentication(self, gmail_connector):
        # Create a mock credentials object
        mock_creds = MagicMock()
        mock_creds.valid = True
        
        # Mock the file operations and flow
        with patch('os.path.exists', return_value=True), \
             patch('builtins.open', MagicMock()), \
             patch('pickle.load', return_value=mock_creds), \
             patch('email_processor.gmail_connector.build') as mock_build:
            
            # Configure the mock build function
            mock_service = MagicMock()
            mock_build.return_value = mock_service
            
            # Test authentication
            result = gmail_connector.authenticate()
            
            assert result == True
            assert gmail_connector.service is not None

    def test_fetch_unread_emails(self, gmail_connector):
        # Mock the Gmail API response
        gmail_connector.service.users().messages().list.return_value.execute.return_value = {
            'messages': [{'id': '12345'}]
        }
        gmail_connector.service.users().messages().get.return_value.execute.return_value = SAMPLE_EMAIL_DATA

        emails = gmail_connector.fetch_unread_emails()
        assert len(emails) == 1
        assert emails[0]['subject'] == 'Update Financial Model'
        assert emails[0]['sender'] == 'sender@example.com'
        assert len(emails[0]['attachments']) == 1

    def test_mark_as_read(self, gmail_connector):
        result = gmail_connector.mark_as_read('12345')
        assert result == True
        gmail_connector.service.users().messages().modify.assert_called_once()

class TestInstructionParser:
    @pytest.fixture
    def mock_llm_provider(self):
        provider = Mock()
        provider.analyze_text.return_value = json.dumps({
            "is_excel_task": True,
            "task_type": "edit_existing",
            "model_name": "Q2_Model.xlsx",
            "required_changes": ["Update revenue projections in Q2"],
            "use_attachment": True,
            "attachment_name": "Q2_Model.xlsx",
            "priority": "high",
            "confidence_score": 0.95
        })
        return provider

    @pytest.fixture
    def instruction_parser(self, mock_llm_provider):
        return InstructionParser(mock_llm_provider)

    def test_parse_email_with_excel_task(self, instruction_parser):
        email_data = {
            'subject': 'Update Financial Model',
            'body': 'Please update the revenue projections in Q2_Model.xlsx',
            'attachments': [{'filename': 'Q2_Model.xlsx'}]
        }

        result = instruction_parser.parse_email(email_data)
        assert result is not None
        assert result['is_excel_task'] == True
        assert result['task_type'] == 'edit_existing'
        assert result['model_name'] == 'Q2_Model.xlsx'

    def test_parse_email_without_excel_task(self, instruction_parser, mock_llm_provider):
        # Mock LLM to return non-Excel task
        mock_llm_provider.analyze_text.return_value = json.dumps({
            "is_excel_task": False,
            "task_type": "none",
            "model_name": None,
            "required_changes": None,
            "use_attachment": False,
            "attachment_name": None,
            "priority": "low",
            "confidence_score": 0.2
        })

        email_data = {
            'subject': 'Team Lunch',
            'body': 'Let\'s get lunch tomorrow',
            'attachments': []
        }

        result = instruction_parser.parse_email(email_data)
        assert result is None

class TestLLMProviders:
    def test_ollama_provider(self):
        # Mock the entire ollama module
        mock_ollama = MagicMock()
        mock_ollama.generate.return_value = {'response': 'mock response'}
        
        with patch.dict('sys.modules', {'ollama': mock_ollama}):
            provider = OllamaProvider()
            provider.ollama = mock_ollama  # Directly set the mocked module
            result = provider.analyze_text("test prompt")
            assert result == 'mock response'

    def test_openai_provider(self):
        # Mock the entire openai module
        mock_openai = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content='mock response'))]
        mock_openai.ChatCompletion.create.return_value = mock_response
        
        with patch.dict('sys.modules', {'openai': mock_openai}):
            provider = OpenAIProvider(api_key="test-key")
            provider.openai = mock_openai  # Directly set the mocked module
            result = provider.analyze_text("test prompt")
            assert result == 'mock response' 
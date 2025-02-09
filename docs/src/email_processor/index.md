# Email Processor Module

## Overview
The email processor module handles email communication through Gmail, including parsing instructions from emails and managing attachments.

## Components

### Gmail Connector (`gmail_connector.py`)
Handles Gmail API integration and email operations:
```python
class GmailConnector:
    def __init__(self, credentials_path: str):
        """Initialize Gmail connection
        
        Args:
            credentials_path: Path to Gmail API credentials file
        """
    
    def authenticate(self) -> None:
        """Authenticate with Gmail API using OAuth2"""
    
    def fetch_emails(self, query: str, max_results: int = 10) -> List[Dict]:
        """Fetch emails matching query
        
        Args:
            query: Gmail search query
            max_results: Maximum number of emails to retrieve
            
        Returns:
            List of email data dictionaries
        """
    
    def get_attachments(self, message_id: str) -> List[Tuple[str, bytes]]:
        """Get attachments from email
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            List of (filename, content) tuples
        """
    
    def send_email(self, 
                  to: str, 
                  subject: str, 
                  body: str,
                  attachments: List[str] = None) -> bool:
        """Send email with optional attachments
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            attachments: Optional list of file paths to attach
            
        Returns:
            True if sent successfully
        """
```

### Instruction Parser (`instruction_parser.py`)
Parses email content for automation instructions:
```python
class InstructionParser:
    def __init__(self, llm_provider: str = "ollama"):
        """Initialize instruction parser
        
        Args:
            llm_provider: LLM provider to use for parsing
        """
    
    def parse_instructions(self, email_content: str) -> Dict:
        """Parse email content for automation instructions
        
        Args:
            email_content: Raw email content
            
        Returns:
            Dictionary of parsed instructions
        """
    
    def validate_instructions(self, instructions: Dict) -> bool:
        """Validate parsed instructions
        
        Args:
            instructions: Parsed instruction dictionary
            
        Returns:
            True if instructions are valid
        """
    
    def extract_parameters(self, instructions: Dict) -> Dict:
        """Extract execution parameters from instructions
        
        Args:
            instructions: Parsed instruction dictionary
            
        Returns:
            Dictionary of execution parameters
        """
```

## Usage Examples

### Email Processing Workflow
```python
# Initialize components
gmail = GmailConnector("credentials.json")
parser = InstructionParser()

# Fetch relevant emails
emails = gmail.fetch_emails("subject:Financial Report")

for email in emails:
    # Get attachments
    attachments = gmail.get_attachments(email["id"])
    
    # Parse instructions from email body
    instructions = parser.parse_instructions(email["body"])
    
    if parser.validate_instructions(instructions):
        # Process according to instructions
        params = parser.extract_parameters(instructions)
        # ... execute automation ...
```

### Sending Results
```python
# After processing
gmail.send_email(
    to="user@example.com",
    subject="Financial Report Processing Complete",
    body="Your report has been processed. Results attached.",
    attachments=["processed_report.xlsx"]
)
```

## Integration Points

### With LLM Providers
- Uses LLM for instruction parsing
- Supports both OpenAI and Ollama
- Configurable parsing templates

### With Excel Handler
- Processes Excel attachments
- Generates Excel reports
- Handles formatted output

### With Error Handler
- Email-specific error handling
- User notification for issues
- Processing status tracking

## Configuration

### Gmail API Setup
```python
{
    "installed": {
        "client_id": "your-client-id",
        "client_secret": "your-client-secret",
        "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    }
}
```

### Instruction Parser Configuration
```python
parser = InstructionParser(
    llm_provider="ollama",
    model="mistral",
    confidence_threshold=0.8
)
```

## Security Considerations
- OAuth2 authentication
- Secure credential storage
- Attachment scanning
- Rate limiting
- Access scope management 
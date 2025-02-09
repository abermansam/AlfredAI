# Email Processor Module

## Overview
The email processor module handles email communication, including reading financial reports from emails and sending automated updates.

## Components

### EmailProcessor
Main class for email operations:
```python
class EmailProcessor:
    def __init__(self, config: EmailConfig):
        """Initialize with email configuration"""
    
    def fetch_financial_emails(self, 
                             since: datetime,
                             filters: Dict[str, str]) -> List[Email]:
        """Fetch financial emails based on criteria"""
    
    def extract_attachments(self, 
                          email: Email,
                          save_path: str) -> List[str]:
        """Extract and save email attachments"""
    
    def send_report(self, 
                   recipients: List[str],
                   subject: str,
                   body: str,
                   attachments: List[str] = None):
        """Send financial report email"""
```

### EmailConfig
Configuration for email processing:
```python
@dataclass
class EmailConfig:
    imap_server: str
    smtp_server: str
    username: str
    password: str
    port: int = 587
    use_ssl: bool = True
```

## Usage Example
```python
# Initialize processor
config = EmailConfig(
    imap_server="imap.gmail.com",
    smtp_server="smtp.gmail.com",
    username="your@email.com",
    password="your_app_password"
)
processor = EmailProcessor(config)

# Fetch financial emails
emails = processor.fetch_financial_emails(
    since=datetime.now() - timedelta(days=7),
    filters={"subject": "Financial Report"}
)

# Process attachments
for email in emails:
    files = processor.extract_attachments(
        email,
        save_path="./reports"
    )

# Send report
processor.send_report(
    recipients=["team@company.com"],
    subject="Weekly Financial Update",
    body="Please find attached the latest financial report.",
    attachments=["report.xlsx"]
)
```

## Security Notes
- Use app-specific passwords for Gmail
- Store credentials securely (use environment variables)
- Enable SSL/TLS for secure connections 
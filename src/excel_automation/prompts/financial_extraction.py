"""
Prompt templates for financial data extraction
"""

FINANCIAL_EXTRACTION_PROMPT = """
Extract financial data from the following text. For each financial item, provide:
- Category (e.g., revenue, expenses, profit)
- Value (numerical amount)
- Date (if mentioned)
- Unit (e.g., USD, EUR)
- Confidence level (0.0-1.0)

Format the response as JSON with the following structure:
{
    "items": [
        {
            "category": "revenue",
            "value": 1200000,
            "date": "2024-02-08",
            "unit": "USD",
            "confidence": 0.95
        }
    ]
}

Text to analyze:
{text}
""" 
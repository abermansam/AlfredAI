"""
Test EDGAR API connection
"""

from excel_automation.edgar_retrieval import EdgarRetriever
from excel_automation.config.edgar_config import EdgarConfig

def main():
    config = EdgarConfig()
    retriever = EdgarRetriever(config)
    
    # Test connection
    if retriever.test_connection():
        print("Successfully connected to EDGAR API")
        
        # Try to get Apple's info
        try:
            apple_info = retriever.get_company_info("AAPL")
            print(f"Found Apple's info: {apple_info}")
        except Exception as e:
            print(f"Error getting company info: {e}")
    else:
        print("Failed to connect to EDGAR API")

if __name__ == "__main__":
    main() 
"""
Test script for EDGAR data retrieval workflow
"""

import os
from excel_automation.data_retrieval.edgar.retriever import EdgarRetriever
from excel_automation.data_retrieval.edgar.config import EdgarConfig
from loguru import logger

def test_edgar_workflow():
    # Initialize retriever with your email
    config = EdgarConfig(
        user_agent="samaberman@live.com"  # Replace with your email
    )
    retriever = EdgarRetriever(config, llm_provider="ollama")  # or "openai" if you prefer
    
    try:
        # Test connection
        logger.info("Testing EDGAR connection...")
        if not retriever.test_connection():
            raise Exception("Failed to connect to EDGAR")
        
        # Test command parsing
        command = "Get Apple's latest 10-K filing and show total assets, revenue, and net income"
        logger.info(f"Parsing command: {command}")
        query = retriever.parse_command(command)
        logger.info(f"Parsed query: {query}")
        
        # Get company info
        logger.info(f"Getting company info for {query.ticker}")
        company_info = retriever.get_company_info(query.ticker)
        logger.info(f"Found company: {company_info}")
        
        # Fetch filing
        logger.info(f"Fetching {query.filing_type} filing...")
        filing_data = retriever.fetch_filing(company_info["cik"], query.filing_type)
        
        # Extract metrics
        logger.info(f"Extracting metrics: {query.metrics}")
        results = retriever.extract_metrics(filing_data, query.metrics)
        
        # Display results
        logger.info("\nResults:")
        for result in results:
            logger.info(f"{result.category}: ${result.value:,.2f} ({result.date})")
            logger.info(f"Source: {result.source}")
            logger.info(f"Confidence: {result.confidence}")
            logger.info(f"Notes: {result.notes}\n")
        
    except Exception as e:
        logger.error(f"Error in workflow: {str(e)}")
        raise

def main():
    # Set up logging
    logger.add("edgar_test.log", rotation="1 MB")
    
    try:
        test_edgar_workflow()
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
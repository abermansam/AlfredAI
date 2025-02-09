"""
Test script for EDGAR metric extraction
"""

from excel_automation.data_retrieval.edgar.retriever import EdgarRetriever
from excel_automation.data_retrieval.edgar.config import EdgarConfig
from loguru import logger

# Sample filing data (you can replace this with real data)
SAMPLE_FILING = {
    "facts": {
        "us-gaap": {
            "Assets": {
                "units": {
                    "USD": [
                        {
                            "end": "2023-09-30",
                            "val": 352755000000
                        },
                        {
                            "end": "2022-09-30",
                            "val": 338215000000
                        }
                    ]
                }
            },
            "Revenues": {
                "units": {
                    "USD": [
                        {
                            "end": "2023-09-30",
                            "val": 383285000000
                        }
                    ]
                }
            },
            "NetIncomeLoss": {
                "units": {
                    "USD": [
                        {
                            "end": "2023-09-30",
                            "val": 96995000000
                        }
                    ]
                }
            }
        }
    }
}

def test_metric_extraction():
    # Initialize retriever
    config = EdgarConfig()
    retriever = EdgarRetriever(config)
    
    # Test metrics to extract
    metrics = [
        "total assets",
        "revenue",
        "net income",
        "nonexistent metric"  # To test error handling
    ]
    
    # Test with specific date
    logger.info("Testing metric extraction with specific date...")
    results = retriever.extract_metrics(SAMPLE_FILING, metrics, "2023-09-30")
    
    logger.info("\nResults for 2023-09-30:")
    for result in results:
        logger.info(f"{result.category}: ${result.value:,.2f}")
        logger.info(f"Date: {result.date}")
        logger.info(f"Notes: {result.notes}\n")
    
    # Test without date (should get most recent)
    logger.info("Testing metric extraction without date...")
    results = retriever.extract_metrics(SAMPLE_FILING, metrics)
    
    logger.info("\nResults (most recent):")
    for result in results:
        logger.info(f"{result.category}: ${result.value:,.2f}")
        logger.info(f"Date: {result.date}")
        logger.info(f"Notes: {result.notes}\n")

def main():
    logger.add("metric_extraction_test.log", rotation="1 MB")
    
    try:
        test_metric_extraction()
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
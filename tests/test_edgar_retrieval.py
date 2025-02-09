"""
Tests for EDGAR data retrieval functionality
"""

import pytest
from excel_automation.data_retrieval.edgar import EdgarRetriever, EdgarConfig, EdgarQuery
from datetime import datetime
import json

class TestEdgarRetrieval:
    @pytest.fixture
    def config(self):
        return EdgarConfig(
            user_agent="alfredAI test@example.com"
        )
    
    @pytest.fixture
    def retriever(self, config):
        return EdgarRetriever(config)
    
    def test_connection(self, retriever, requests_mock):
        # Mock the company tickers endpoint
        mock_data = {
            "0": {
                "cik_str": 320193,
                "ticker": "AAPL",
                "title": "Apple Inc."
            }
        }
        
        requests_mock.get(
            "https://www.sec.gov/files/company_tickers.json",
            json=mock_data
        )
        
        assert retriever.test_connection() == True
    
    def test_get_company_info(self, retriever, requests_mock):
        # Mock company lookup response
        mock_data = {
            "0": {
                "cik_str": 320193,
                "ticker": "AAPL",
                "title": "Apple Inc."
            }
        }
        
        requests_mock.get(
            "https://www.sec.gov/files/company_tickers.json",
            json=mock_data
        )
        
        result = retriever.get_company_info("AAPL")
        assert result["cik"] == "0000320193"
        assert result["name"] == "Apple Inc."
        assert result["ticker"] == "AAPL"
    
    def test_parse_command(self, retriever, mocker):
        # Mock LLM response
        mock_response = {
            "company_name": "Apple Inc.",
            "ticker": "AAPL",
            "filing_type": "10-K",
            "filing_date": "latest",
            "metrics": ["total assets", "total liabilities", "net income"]
        }
        
        # Mock the LLM provider
        mock_llm = mocker.Mock()
        mock_llm.complete.return_value = json.dumps(mock_response)
        retriever.llm = mock_llm
        
        command = "Retrieve the latest 10-K filing for Apple Inc. (AAPL) and extract total assets, total liabilities, and net income"
        query = retriever.parse_command(command)
        
        assert query.company_name == "Apple Inc."
        assert query.ticker == "AAPL"
        assert query.filing_type == "10-K"
        assert query.filing_date is None  # "latest" becomes None
        assert set(query.metrics) == {"total assets", "total liabilities", "net income"}
        
        # Verify LLM was called with correct prompt
        mock_llm.complete.assert_called_once()
        prompt_arg = mock_llm.complete.call_args[0][0]
        assert command in prompt_arg

    def test_parse_command_with_date(self, retriever, mocker):
        # Mock LLM response with specific date
        mock_response = {
            "company_name": "Apple Inc.",
            "ticker": "AAPL",
            "filing_type": "10-K",
            "filing_date": "2023-09-30",
            "metrics": ["total assets"]
        }
        
        mock_llm = mocker.Mock()
        mock_llm.complete.return_value = json.dumps(mock_response)
        retriever.llm = mock_llm
        
        command = "Get the September 2023 10-K filing for Apple Inc. and show total assets"
        query = retriever.parse_command(command)
        
        assert query.company_name == "Apple Inc."
        assert query.filing_date == datetime(2023, 9, 30)
    
    def test_fetch_filing(self, retriever, requests_mock):
        # Mock SEC API response
        mock_data = {
            "cik": 320193,
            "entityName": "Apple Inc.",
            "facts": {
                "us-gaap": {
                    "Assets": {
                        "units": {
                            "USD": [
                                {
                                    "end": "2023-09-30",
                                    "val": 352755000000
                                }
                            ]
                        }
                    }
                }
            }
        }
        
        requests_mock.get(
            "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json",
            json=mock_data
        )
        
        result = retriever.fetch_filing("320193", "10-K")
        assert result["entityName"] == "Apple Inc."
        assert result["facts"]["us-gaap"]["Assets"]["units"]["USD"][0]["val"] == 352755000000 

    def test_extract_metrics(self, retriever):
        # Mock filing data
        filing_data = {
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
                    }
                }
            }
        }
        
        # Test with specific date
        metrics = ["total assets", "revenue"]
        results = retriever.extract_metrics(filing_data, metrics, "2023-09-30")
        
        assert len(results) == 2
        
        assets = next(r for r in results if r.category == "total assets")
        assert assets.value == 352755000000
        assert assets.date == datetime(2023, 9, 30)
        assert assets.unit == "USD"
        
        revenue = next(r for r in results if r.category == "revenue")
        assert revenue.value == 383285000000

    def test_extract_metrics_missing_data(self, retriever):
        # Mock filing data with missing metrics
        filing_data = {
            "facts": {
                "us-gaap": {
                    "Assets": {
                        "units": {
                            "USD": [
                                {
                                    "end": "2023-09-30",
                                    "val": 352755000000
                                }
                            ]
                        }
                    }
                }
            }
        }
        
        # Test with missing metric
        metrics = ["total assets", "nonexistent metric"]
        results = retriever.extract_metrics(filing_data, metrics, "2023-09-30")
        
        assert len(results) == 1
        assert results[0].category == "total assets"

    def test_extract_metrics_date_fallback(self, retriever):
        # Mock filing data with multiple dates
        filing_data = {
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
                    }
                }
            }
        }
        
        # Test without specific date (should get most recent)
        results = retriever.extract_metrics(filing_data, ["total assets"])
        
        assert len(results) == 1
        assert results[0].value == 352755000000  # Should get most recent value 
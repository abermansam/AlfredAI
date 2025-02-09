"""
EDGAR Data Retrieval Module
"""

from typing import Dict, List, Optional
from loguru import logger
import requests
import json
from datetime import datetime
import time

from ..base import DataRetriever, FinancialData
from .config import EdgarConfig
from .models import EdgarQuery
from .prompts import EDGAR_COMMAND_PARSE_PROMPT
from ..providers.llm import get_llm_provider
from .metrics import normalize_metric_name, get_metric_value

class EdgarRetriever(DataRetriever):
    """Handles retrieval of financial data from EDGAR"""
    
    def __init__(self, config: Optional[EdgarConfig] = None, llm_provider: str = "openai"):
        """Initialize with configuration"""
        super().__init__(config or EdgarConfig())
        self.headers = {
            "User-Agent": self.config.user_agent,
            "Accept": "application/json",
        }
        self.llm = get_llm_provider(llm_provider)
    
    def test_connection(self) -> bool:
        """Test connection to EDGAR API"""
        try:
            response = requests.get(
                self.config.company_search_url,
                headers=self.headers
            )
            response.raise_for_status()
            
            time.sleep(self.config.rate_limit_sleep)
            logger.info("Successfully connected to EDGAR API")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to EDGAR API: {str(e)}")
            return False
    
    def get_company_info(self, ticker: str) -> Dict:
        """Get company CIK and other info using ticker"""
        try:
            response = requests.get(
                self.config.company_search_url,
                headers=self.headers
            )
            response.raise_for_status()
            companies = response.json()
            
            for cik, company in companies.items():
                if company['ticker'].upper() == ticker.upper():
                    return {
                        'cik': str(company['cik_str']).zfill(10),
                        'name': company['title'],
                        'ticker': company['ticker']
                    }
            
            raise ValueError(f"Company with ticker {ticker} not found")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching company info: {str(e)}")
            raise
    
    def parse_command(self, command: str) -> EdgarQuery:
        """Parse plain English command into structured query"""
        try:
            prompt = EDGAR_COMMAND_PARSE_PROMPT.format(command=command)
            response = self.llm.complete(prompt)
            
            try:
                parsed = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON response from LLM: {response}")
                raise ValueError(f"Failed to parse LLM response as JSON: {str(e)}")
            
            return EdgarQuery(
                company_name=parsed["company_name"],
                ticker=parsed.get("ticker"),
                cik=None,
                filing_type=parsed["filing_type"],
                filing_date=datetime.strptime(parsed["filing_date"], "%Y-%m-%d") 
                    if parsed.get("filing_date") and parsed["filing_date"] != "latest" 
                    else None,
                metrics=parsed["metrics"]
            )
            
        except KeyError as e:
            logger.error(f"Missing required field in LLM response: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error parsing command: {str(e)}")
            raise
    
    def fetch_filing(self, cik: str, filing_type: str) -> Dict:
        """Fetch specific filing data from EDGAR"""
        cik_padded = str(cik).zfill(10)
        url = f"{self.config.base_url}/CIK{cik_padded}.json"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching EDGAR data: {str(e)}")
            raise
    
    def extract_metrics(self, filing_data: Dict, metrics: List[str], filing_date: Optional[str] = None) -> List[FinancialData]:
        """Extract requested metrics from filing data"""
        results = []
        
        for metric in metrics:
            # Get XBRL tag for metric
            xbrl_tag = normalize_metric_name(metric)
            if not xbrl_tag:
                logger.warning(f"No XBRL mapping found for metric: {metric}")
                continue
            
            # Extract value
            value = get_metric_value(filing_data, xbrl_tag, filing_date)
            if value is None:
                logger.warning(f"Could not find value for metric: {metric} ({xbrl_tag})")
                continue
            
            # Create FinancialData object
            financial_data = FinancialData(
                source="EDGAR",
                date=datetime.strptime(filing_date, "%Y-%m-%d") if filing_date else datetime.now(),
                category=metric,
                value=float(value),
                confidence=1.0,  # High confidence for EDGAR data
                unit="USD",
                notes=f"XBRL tag: {xbrl_tag}"
            )
            
            results.append(financial_data)
        
        return results 
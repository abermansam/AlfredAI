"""
Tests for base data retrieval functionality
"""

import pytest
from excel_automation.data_retrieval import DataRetriever, FinancialData
from datetime import datetime

def test_financial_data_creation():
    """Test FinancialData dataclass"""
    data = FinancialData(
        source="test",
        date=datetime.now(),
        category="revenue",
        value=1000.0,
        confidence=0.95,
        unit="USD",
        notes="Test note"
    )
    
    assert data.source == "test"
    assert data.value == 1000.0
    assert data.unit == "USD"
    assert data.confidence == 0.95

def test_data_retriever_base():
    """Test base DataRetriever class"""
    class TestConfig:
        pass
    
    retriever = DataRetriever(TestConfig())
    assert retriever.config is not None

class TestDataRetrieval:
    @pytest.fixture
    def retriever(self):
        return DataRetriever()
    
    def test_extract_from_text(self, retriever):
        sample_text = """
        Q2 2024 Financial Results:
        Revenue: $1.2M
        Operating Expenses: $800K
        Net Income: $400K
        """
        
        results = retriever.extract_from_text(sample_text)
        assert len(results) == 3
        assert all(isinstance(r, FinancialData) for r in results)
        
    def test_data_validation(self, retriever):
        valid_data = FinancialData(
            source="quarterly_report",
            date=datetime.now(),
            category="revenue",
            value=1200000.0,
            confidence=0.95,
            unit="USD"
        )
        
        assert retriever.validate_data(valid_data) == True 
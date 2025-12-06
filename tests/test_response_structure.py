"""
Response structure validation tests.
"""
import pytest
from src.validators.response_validator import ResponseValidator


@pytest.mark.regression
class TestResponseStructure:
    """Test response structure and schema validation."""
    
    def test_response_has_data_field(self, sample_response):
        """Test that response contains 'data' field."""
        assert 'data' in sample_response, "Response missing 'data' field"
    
    def test_response_has_answer_field(self, sample_response):
        """Test that response data contains 'answer' field."""
        assert 'answer' in sample_response['data'], "Response data missing 'answer' field"
    
    def test_answer_is_string(self, sample_response):
        """Test that answer field is a string."""
        answer = sample_response['data']['answer']
        assert isinstance(answer, str), f"Answer must be string, got {type(answer).__name__}"
    
    def test_answer_not_empty(self, sample_response):
        """Test that answer is not empty."""
        answer = sample_response['data']['answer']
        assert len(answer.strip()) > 0, "Answer is empty"
    
    def test_response_has_metadata(self, sample_response):
        """Test that response includes metadata fields."""
        assert 'status_code' in sample_response, "Response missing 'status_code'"
        assert 'response_time' in sample_response, "Response missing 'response_time'"
        assert 'question' in sample_response, "Response missing 'question'"
    
    def test_response_validation_passes(self, sample_response):
        """Test that response passes complete validation."""
        is_valid, errors = ResponseValidator.validate_response(sample_response)
        assert is_valid, f"Response validation failed: {', '.join(errors)}"
    
    def test_answer_minimum_length(self, sample_response):
        """Test that answer meets minimum length requirement."""
        answer = sample_response['data']['answer']
        min_length = 100
        assert len(answer) >= min_length, \
            f"Answer length {len(answer)} is below minimum {min_length}"

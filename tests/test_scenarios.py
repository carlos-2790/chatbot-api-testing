"""
Scenario-based tests with different questions.
"""
import pytest
import json
from pathlib import Path
from src.validators.quality_scorer import QualityScorer
from src.utils.config import Config


# Load test questions
test_data_path = Config.DATA_DIR / 'test_questions.json'
with open(test_data_path, 'r', encoding='utf-8') as f:
    test_questions_data = json.load(f)

# Extract questions for parametrization
test_questions = [item['question'] for item in test_questions_data]


@pytest.mark.regression
@pytest.mark.parametrize("question", test_questions)
class TestScenarios:
    """Test various question scenarios."""
    
    def test_question_gets_valid_response(self, api_client, question):
        """Test that each question gets a valid response."""
        response = api_client.ask(question)
        assert response['status_code'] == 200, \
            f"Failed to get valid response for: {question}"
        assert 'answer' in response['data'], \
            f"No answer in response for: {question}"
    
    def test_question_meets_quality_threshold(self, api_client, question, quality_scorer):
        """Test that each question's response meets quality threshold."""
        response = api_client.ask(question)
        overall_score = quality_scorer.calculate_overall_score(response, question)
        threshold = Config.QUALITY_THRESHOLD
        
        assert overall_score >= threshold, \
            f"Question '{question}' failed quality check: {overall_score:.2f} < {threshold}"
    
    def test_question_response_time(self, api_client, question):
        """Test that each question responds within acceptable time."""
        response = api_client.ask(question)
        max_time = 5.0
        assert response['response_time'] < max_time, \
            f"Question '{question}' took too long: {response['response_time']:.2f}s > {max_time}s"


@pytest.mark.quality
class TestSpecificScenarios:
    """Test specific important scenarios."""
    
    def test_python_unittest_question(self, api_client, quality_scorer):
        """Test question about Python unit testing."""
        question = "¿Cómo escribir tests unitarios en Python?"
        response = api_client.ask(question)
        
        scores = quality_scorer.get_detailed_scores(response, question)
        
        # Should mention pytest or unittest
        answer = response['data']['answer'].lower()
        assert 'pytest' in answer or 'unittest' in answer, \
            "Response should mention pytest or unittest"
        
        # Should pass quality threshold
        assert scores['passes_threshold'], \
            f"Quality score {scores['overall_score']:.2f} below threshold"
    
    def test_mocking_question(self, api_client, quality_scorer):
        """Test question about mocking."""
        question = "¿Qué es mocking y cuándo usarlo?"
        response = api_client.ask(question)
        
        answer = response['data']['answer'].lower()
        
        # Should mention mock-related concepts
        mock_keywords = ['mock', 'stub', 'fake', 'dependency']
        mentions_mocking = any(keyword in answer for keyword in mock_keywords)
        assert mentions_mocking, "Response should mention mocking concepts"
        
        # Should pass quality threshold
        passes = quality_scorer.validate_quality(response, question)
        assert passes, "Mocking question should pass quality validation"
    
    def test_tdd_question(self, api_client, quality_scorer):
        """Test question about TDD."""
        question = "¿Qué es TDD y cómo implementarlo?"
        response = api_client.ask(question)
        
        answer = response['data']['answer'].lower()
        
        # Should mention TDD concepts
        tdd_keywords = ['tdd', 'test-driven', 'red', 'green', 'refactor']
        mentions_tdd = any(keyword in answer for keyword in tdd_keywords)
        assert mentions_tdd, "Response should mention TDD concepts"
        
        # Should pass quality threshold
        scores = quality_scorer.get_detailed_scores(response, question)
        assert scores['passes_threshold'], \
            f"TDD question quality score {scores['overall_score']:.2f} below threshold"

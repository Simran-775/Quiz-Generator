from project import get_topic,generate_quiz,wikipedia_fetch
import pytest

def test_get_topic():
    assert get_topic("  python   ") == "Python"
    assert get_topic("python") == "Python"
    assert get_topic("hello") == "Not valid"

def test_wikipedia():
    result = wikipedia_fetch("Python")
    assert result is not None
    assert "Python" in result

def test_generate_quiz():
    result = wikipedia_fetch("Python")
    quiz = generate_quiz(result,3)
    assert isinstance(quiz,list)
    assert len(quiz) <= 3
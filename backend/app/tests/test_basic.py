"""
Simple test to verify the testing setup works.
"""
import pytest

def test_basic_assertion():
    """A simple test to verify pytest is working."""
    assert 1 + 1 == 2

def test_string_operations():
    """Test string operations."""
    hello = "Hello, World!"
    assert hello.startswith("Hello")
    assert hello.endswith("World!")
    assert len(hello) == 13
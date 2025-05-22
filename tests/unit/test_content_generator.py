"""
Unit tests for the content generator module.
"""

import pytest
from copilot_tester.content_generator import generate_random_markdown_content


def test_generate_random_markdown_content():
    """Test the random markdown content generator."""
    # Test with different sizes
    for size_kb in [1, 5, 10]:
        content = generate_random_markdown_content(size_kb)

        # Check that the content is approximately the expected size
        # Allow for some variation due to trimming at exact boundaries
        expected_size = size_kb * 1024
        assert (
            abs(len(content) - expected_size) < 5
        ), f"Content size {len(content)} not close to expected {expected_size}"

        # Check that the content contains expected markdown elements
        assert "#" in content, "Content should contain headings"
        assert "```python" in content, "Content should contain code blocks"
        assert "|" in content, "Content should contain tables"

"""
Content generator module for creating test content.

This module provides functionality to generate random markdown content
of varying sizes for testing purposes.
"""

import random
import string


def generate_random_markdown_content(size_kb):
    """Generate random markdown content of approximately the specified size in KB.

    Args:
        size_kb (int): Target size of the content in kilobytes

    Returns:
        str: Randomly generated markdown content
    """
    # 1 KB is roughly 1024 characters
    chars_needed = size_kb * 1024

    # Create sections to make it look like a real document
    sections = []
    chars_generated = 0

    while chars_generated < chars_needed:
        # Create a heading
        heading_level = random.randint(1, 3)
        heading = (
            "#" * heading_level
            + " "
            + "".join(random.choices(string.ascii_letters, k=random.randint(5, 20)))
        )

        # Create paragraphs
        paragraphs = []
        for _ in range(random.randint(1, 5)):
            paragraph_length = random.randint(100, 500)
            paragraph = " ".join(
                "".join(
                    random.choices(
                        string.ascii_lowercase + " ", k=random.randint(3, 10)
                    )
                )
                for _ in range(paragraph_length // 5)
            )
            paragraphs.append(paragraph)

        # Create a code block
        code_block = "```python\n"
        for _ in range(random.randint(5, 20)):
            code_block += (
                "def function_"
                + "".join(random.choices(string.ascii_lowercase, k=5))
                + "():\n"
            )
            code_block += (
                "    "
                + "return "
                + "".join(random.choices(string.ascii_lowercase, k=8))
                + "\n"
            )
        code_block += "```\n"

        # Create a table
        table = "| " + " | ".join("Header" + str(i) for i in range(1, 6)) + " |\n"
        table += "| " + " | ".join("---" for _ in range(5)) + " |\n"
        for _ in range(random.randint(3, 8)):
            table += (
                "| "
                + " | ".join(
                    "".join(
                        random.choices(string.ascii_lowercase, k=random.randint(5, 10))
                    )
                    for _ in range(5)
                )
                + " |\n"
            )

        # Assemble section
        section = (
            heading
            + "\n\n"
            + "\n\n".join(paragraphs)
            + "\n\n"
            + code_block
            + "\n"
            + table
            + "\n\n"
        )
        sections.append(section)

        chars_generated += len(section)

    return "".join(sections)[:chars_needed]  # Trim to exact size

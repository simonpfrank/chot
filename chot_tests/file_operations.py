"""
File operations module for creating and manipulating test files.

This module provides functionality to create test files, inject patterns,
and split test cases into batches.
"""

import os
import re
from typing import List, Tuple, Dict, Any

from copilot_tester.content_generator import generate_random_markdown_content


def create_test_files(
    sizes_kb: List[int] = [10, 50, 100, 200, 500, 1000],
    base_dir: str = "response_test_files",
) -> List[Tuple[str, int]]:
    """Create test files of various sizes to test response limits.

    Args:
        sizes_kb: List of file sizes in KB to generate
        base_dir: Directory to store the generated files

    Returns:
        List of tuples containing (filename, size_kb)
    """
    os.makedirs(base_dir, exist_ok=True)

    created_files = []
    for size in sizes_kb:
        filename = f"{base_dir}/test_file_{size}kb.md"
        with open(filename, "w", encoding="utf-8") as f:
            content = generate_random_markdown_content(size)
            f.write(content)
        created_files.append((filename, size))
        print(f"Created test file: {filename} ({size} KB)")

    return created_files


def create_edit_patterns(
    num_edits: List[int] = [1, 2, 5, 10, 20]
) -> List[Dict[str, Any]]:
    """Generate patterns of edits to test multiple tool calls.

    Args:
        num_edits: List of edit counts to generate patterns for

    Returns:
        List of pattern dictionaries
    """
    patterns = []

    for n in num_edits:
        # Create a pattern that has n edits
        pattern = {"name": f"pattern_{n}_edits", "replacements": []}

        # Generate n unique replacements
        for i in range(n):
            # Create unique markers that can be found and replaced
            original = f"<!--UNIQUE_MARKER_{i}_START-->\nThis is original text {i}\n<!--UNIQUE_MARKER_{i}_END-->"
            replacement = f"<!--UNIQUE_MARKER_{i}_START-->\nThis is replacement text {i}\n<!--UNIQUE_MARKER_{i}_END-->"

            pattern["replacements"].append(
                {"original": original, "replacement": replacement}
            )

        patterns.append(pattern)

    return patterns


def inject_patterns_into_files(
    files: List[Tuple[str, int]],
    patterns: List[Dict[str, Any]],
    output_dir: str = "response_test_files_with_patterns",
) -> List[Dict[str, Any]]:
    """Inject the edit patterns into the test files.

    Args:
        files: List of (filename, size) tuples
        patterns: List of pattern dictionaries
        output_dir: Directory to store the files with injected patterns

    Returns:
        List of test case dictionaries
    """
    os.makedirs(output_dir, exist_ok=True)

    test_cases = []
    for filename, size in files:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        for pattern in patterns:
            # Create a new file with the pattern injected
            pattern_filename = os.path.join(
                output_dir,
                f"{os.path.basename(filename).replace('.md', '')}_{pattern['name']}.md",
            )

            # Inject all the replacements at different positions
            modified_content = content
            chunk_size = len(content) // (len(pattern["replacements"]) + 1)

            for i, replacement in enumerate(pattern["replacements"]):
                insert_pos = (i + 1) * chunk_size
                modified_content = (
                    modified_content[:insert_pos]
                    + "\n\n"
                    + replacement["original"]
                    + "\n\n"
                    + modified_content[insert_pos:]
                )

            with open(pattern_filename, "w", encoding="utf-8") as f:
                f.write(modified_content)

            test_cases.append(
                {
                    "filename": pattern_filename,
                    "file_size_kb": size,
                    "num_edits": len(pattern["replacements"]),
                    "pattern_name": pattern["name"],
                }
            )
            print(f"Created test case: {pattern_filename}")

    # Write test case index
    with open(os.path.join(output_dir, "test_cases.md"), "w", encoding="utf-8") as f:
        f.write("# Test Cases for GitHub Copilot Response Testing\n\n")
        f.write("| Filename | File Size (KB) | Number of Edits | Pattern Name |\n")
        f.write("|----------|---------------|----------------|-------------|\n")
        for case in test_cases:
            f.write(
                f"| {os.path.basename(case['filename'])} | {case['file_size_kb']} | {case['num_edits']} | {case['pattern_name']} |\n"
            )

    return test_cases


def create_batched_test_files(
    test_case: Dict[str, Any],
    max_edits_per_batch: int = 3,
    output_dir: str = "batched_test_files",
) -> List[Dict[str, Any]]:
    """Split a test case with many edits into multiple files with fewer edits per file.

    This helps test whether splitting edits across multiple requests helps avoid timeouts.

    Args:
        test_case: A test case dictionary containing the filename and pattern information
        max_edits_per_batch: Maximum number of edits to include in each batched file
        output_dir: Directory to store the batched files

    Returns:
        List of dictionaries with information about each batched file
    """
    os.makedirs(output_dir, exist_ok=True)

    # Read the original test file
    with open(test_case["filename"], "r", encoding="utf-8") as f:
        content = f.read()

    # Find all the markers in the content
    markers = re.findall(r"<!--UNIQUE_MARKER_(\d+)_START-->", content)
    markers = sorted([int(m) for m in markers])

    # If there aren't more edits than the max per batch, return the original file info
    if len(markers) <= max_edits_per_batch:
        return [test_case]

    # Split into batches
    batches = []
    for batch_idx, i in enumerate(range(0, len(markers), max_edits_per_batch)):
        batch_markers = markers[i : i + max_edits_per_batch]

        # Create a new filename for the batch
        base_name = os.path.basename(test_case["filename"]).replace(".md", "")
        batch_filename = os.path.join(output_dir, f"{base_name}_batch{batch_idx+1}.md")

        # Create a new content file that only has the markers for this batch
        batch_content = content
        removed_markers = [m for m in markers if m not in batch_markers]

        # Remove markers not in this batch
        for marker in removed_markers:
            # Fix: Use a more precise pattern that accounts for the newlines
            marker_pattern = rf"\n\n<!--UNIQUE_MARKER_{marker}_START-->.*?<!--UNIQUE_MARKER_{marker}_END-->\n\n"
            batch_content = re.sub(marker_pattern, "", batch_content, flags=re.DOTALL)

        # Write the batch file
        with open(batch_filename, "w", encoding="utf-8") as f:
            f.write(batch_content)

        batches.append(
            {
                "filename": batch_filename,
                "file_size_kb": test_case["file_size_kb"],
                "num_edits": len(batch_markers),
                "pattern_name": f"{test_case['pattern_name']}_batch{batch_idx+1}",
                "original_test_case": test_case["filename"],
                "batch_markers": batch_markers,
            }
        )

        print(
            f"Created batched test file: {batch_filename} with {len(batch_markers)} edits"
        )

    return batches

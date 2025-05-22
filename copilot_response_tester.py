# GitHub Copilot Response Limit Tester

"""
This script helps test the limits of GitHub Copilot's response handling
by creating large files and complex patterns that can be used to determine
where response timeouts or size limits occur.
"""

import os
import random
import string
import time


def generate_random_markdown_content(size_kb):
    """Generate random markdown content of approximately the specified size in KB."""
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


def create_test_files(
    sizes_kb=[10, 50, 100, 200, 500, 1000], base_dir="response_test_files"
):
    """Create test files of various sizes to test response limits."""
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


def create_edit_patterns(num_edits=[1, 2, 5, 10, 20]):
    """Generate patterns of edits to test multiple tool calls."""
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
    files, patterns, output_dir="response_test_files_with_patterns"
):
    """Inject the edit patterns into the test files."""
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
    test_case, max_edits_per_batch=3, output_dir="batched_test_files"
):
    """Split a test case with many edits into multiple files with fewer edits per file.

    This helps test whether splitting edits across multiple requests helps avoid timeouts.

    Args:
        test_case (dict): A test case dictionary containing the filename and pattern information
        max_edits_per_batch (int): Maximum number of edits to include in each batched file
        output_dir (str): Directory to store the batched files

    Returns:
        list: List of dictionaries with information about each batched file
    """
    os.makedirs(output_dir, exist_ok=True)

    # Read the original test file
    with open(test_case["filename"], "r", encoding="utf-8") as f:
        content = f.read()

    # Find all the markers in the content
    import re

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
            marker_pattern = f"<!--UNIQUE_MARKER_{marker}_START-->.*?<!--UNIQUE_MARKER_{marker}_END-->"
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


if __name__ == "__main__":
    # Check if we should create batches or regular test files
    import sys

    create_batches = "--batch" in sys.argv
    max_edits_per_batch = 3  # Default value

    # Parse batch size if specified
    if create_batches:
        for arg in sys.argv:
            if arg.startswith("--batch-size="):
                try:
                    max_edits_per_batch = int(arg.split("=")[1])
                    print(f"Setting max edits per batch to {max_edits_per_batch}")
                except (ValueError, IndexError):
                    print("Invalid batch size specified, using default of 3")

    # Create base test files of different sizes
    files = create_test_files()

    # Create edit patterns with different numbers of replacements
    patterns = create_edit_patterns()

    # Combine files and patterns to create test cases
    test_cases = inject_patterns_into_files(files, patterns)

    # Create batched versions for test cases with many edits if requested
    if create_batches:
        batched_test_cases = []
        for test_case in test_cases:
            if test_case["num_edits"] > max_edits_per_batch:
                print(
                    f"Creating batched versions of {test_case['filename']} with {test_case['num_edits']} edits..."
                )
                batches = create_batched_test_files(test_case, max_edits_per_batch)
                batched_test_cases.extend(batches)

        if batched_test_cases:
            print(
                f"\nCreated {len(batched_test_cases)} batched test files to help with testing larger edit counts."
            )
            print(
                "These files contain the same content but with fewer markers per file."
            )

    print(
        f"\nCreated {len(test_cases)} test cases to help identify GitHub Copilot response limits."
    )
    print("To use these tests:")
    print("1. Open a test file in VS Code")
    print(
        "2. Ask GitHub Copilot to make all the replacements marked by UNIQUE_MARKER comments"
    )
    print(
        "3. Observe if the response is complete or if you get timeout/size limit errors"
    )
    print("4. Record which combinations of file size and edit count cause issues")

    if create_batches:
        print("\nFor tests with many edits:")
        print(
            f"- Batched versions with max {max_edits_per_batch} edits per file are available in the 'batched_test_files' directory"
        )
        print(
            "- Try these to see if splitting edits into smaller batches helps avoid timeouts"
        )

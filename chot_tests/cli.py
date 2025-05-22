"""
Command-line interface for GitHub Copilot Response Tester.

This module provides a CLI for running the Copilot Response Tester tool.
"""

import sys
import argparse
from typing import List, Optional

from copilot_tester.file_operations import (
    create_test_files,
    create_edit_patterns,
    inject_patterns_into_files,
    create_batched_test_files,
)


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: Command-line arguments (uses sys.argv if not provided)

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="GitHub Copilot Response Limit Tester",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--batch", action="store_true", help="Create batched versions of test files"
    )

    parser.add_argument(
        "--batch-size", type=int, default=3, help="Maximum number of edits per batch"
    )

    parser.add_argument(
        "--sizes",
        type=int,
        nargs="+",
        default=[10, 50, 100, 200, 500, 1000],
        help="List of file sizes in KB to generate",
    )

    parser.add_argument(
        "--edits",
        type=int,
        nargs="+",
        default=[1, 2, 5, 10, 20],
        help="List of edit counts to generate patterns for",
    )

    return parser.parse_args(args)


def main(args: Optional[List[str]] = None) -> None:
    """Main entry point for the CLI.

    Args:
        args: Command-line arguments (uses sys.argv if not provided)
    """
    parsed_args = parse_args(args)

    # Create base test files of different sizes
    files = create_test_files(sizes_kb=parsed_args.sizes)

    # Create edit patterns with different numbers of replacements
    patterns = create_edit_patterns(num_edits=parsed_args.edits)

    # Combine files and patterns to create test cases
    test_cases = inject_patterns_into_files(files, patterns)

    # Create batched versions for test cases with many edits if requested
    if parsed_args.batch:
        batched_test_cases = []
        for test_case in test_cases:
            if test_case["num_edits"] > parsed_args.batch_size:
                print(
                    f"Creating batched versions of {test_case['filename']} with {test_case['num_edits']} edits..."
                )
                batches = create_batched_test_files(test_case, parsed_args.batch_size)
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

    if parsed_args.batch:
        print("\nFor tests with many edits:")
        print(
            f"- Batched versions with max {parsed_args.batch_size} edits per file are available in the 'batched_test_files' directory"
        )
        print(
            "- Try these to see if splitting edits into smaller batches helps avoid timeouts"
        )


if __name__ == "__main__":
    main()

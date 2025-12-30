"""
Command-line interface for the debate algorithm.

This module provides the CLI entry point when the package is installed.
"""

from hardstucks_debating.main import main as _main


def main():
    """CLI entry point."""
    _main()


if __name__ == "__main__":
    main()
